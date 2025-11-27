from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.crud.category import category_crud
from app.dependencies import get_current_active_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all categories."""
    categories = category_crud.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get category by ID."""
    category = category_crud.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Create new category (Admin only)."""
    # Check if category exists
    if category_crud.get_by_name(db, name=category_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    category = category_crud.create(db, category_in)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Update category (Admin only)."""
    category = category_crud.update(db, category_id, category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Delete category (Admin only)."""
    success = category_crud.delete(db, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None

