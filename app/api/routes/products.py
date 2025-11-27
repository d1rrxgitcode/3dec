from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.crud.product import product_crud
from app.crud.category import category_crud
from app.dependencies import get_current_active_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    available_only: bool = False,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filters."""
    if search:
        products = product_crud.search(db, query=search, skip=skip, limit=limit)
    elif category_id:
        products = product_crud.get_by_category(db, category_id=category_id, skip=skip, limit=limit)
    elif available_only:
        products = product_crud.get_available(db, skip=skip, limit=limit)
    else:
        products = product_crud.get_multi(db, skip=skip, limit=limit)
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID."""
    product = product_crud.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Create new product (Admin only)."""
    # Check if category exists
    if not category_crud.get(db, product_in.category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    product = product_crud.create(db, product_in)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Update product (Admin only)."""
    # Check if category exists (if updating category_id)
    if product_in.category_id and not category_crud.get(db, product_in.category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    product = product_crud.update(db, product_id, product_in)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Delete product (Admin only)."""
    success = product_crud.delete(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return None

