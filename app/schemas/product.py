from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    is_available: bool = True
    stock_quantity: int = Field(default=0, ge=0)
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

