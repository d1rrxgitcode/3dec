from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    price: float
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    delivery_address: str
    phone: str
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

