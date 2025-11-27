from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductCRUD:
    def get(self, db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return db.query(Product).filter(Product.id == product_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get multiple products."""
        return db.query(Product).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products by category."""
        return db.query(Product).filter(Product.category_id == category_id).offset(skip).limit(limit).all()

    def get_available(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get available products."""
        return db.query(Product).filter(Product.is_available == True).offset(skip).limit(limit).all()

    def search(self, db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name."""
        return db.query(Product).filter(Product.name.ilike(f"%{query}%")).offset(skip).limit(limit).all()

    def create(self, db: Session, product_in: ProductCreate) -> Product:
        """Create new product."""
        db_product = Product(**product_in.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update(self, db: Session, product_id: int, product_in: ProductUpdate) -> Optional[Product]:
        """Update product."""
        db_product = self.get(db, product_id)
        if not db_product:
            return None
        
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product

    def delete(self, db: Session, product_id: int) -> bool:
        """Delete product."""
        db_product = self.get(db, product_id)
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True


product_crud = ProductCRUD()

