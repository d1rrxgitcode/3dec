from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate
from app.crud.product import product_crud


class OrderCRUD:
    def get(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).offset(skip).limit(limit).all()

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).filter(Order.status == status).offset(skip).limit(limit).all()

    def create(self, db: Session, user_id: int, order_in: OrderCreate) -> Optional[Order]:
        total_amount = 0.0
        order_items_data = []

        for item in order_in.items:
            product = product_crud.get(db, item.product_id)
            if not product:
                return None
            if not product.is_available:
                return None
            if product.stock_quantity < item.quantity:
                return None
            
            item_price = product.price * item.quantity
            total_amount += item_price
            
            order_items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product.price
            })
            
            product.stock_quantity -= item.quantity

        db_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            delivery_address=order_in.delivery_address,
            phone=order_in.phone,
            notes=order_in.notes
        )
        db.add(db_order)
        db.flush()

        for item_data in order_items_data:
            db_order_item = OrderItem(order_id=db_order.id, **item_data)
            db.add(db_order_item)

        db.commit()
        db.refresh(db_order)
        return db_order

    def update(self, db: Session, order_id: int, order_in: OrderUpdate) -> Optional[Order]:
        db_order = self.get(db, order_id)
        if not db_order:
            return None
        
        update_data = order_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        return db_order

    def cancel(self, db: Session, order_id: int) -> Optional[Order]:
        db_order = self.get(db, order_id)
        if not db_order:
            return None
        
        if db_order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            return None
        
        for item in db_order.order_items:
            product = product_crud.get(db, item.product_id)
            if product:
                product.stock_quantity += item.quantity
        
        db_order.status = OrderStatus.CANCELLED
        db.commit()
        db.refresh(db_order)
        return db_order

    def delete(self, db: Session, order_id: int) -> bool:
        db_order = self.get(db, order_id)
        if not db_order:
            return False
        
        db.delete(db_order)
        db.commit()
        return True


order_crud = OrderCRUD()