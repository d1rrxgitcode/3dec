from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.crud.order import order_crud
from app.dependencies import get_current_user, get_current_active_admin
from app.models.user import User
from app.models.order import OrderStatus

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[OrderStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get orders. Users see their own orders, admins see all."""
    if current_user.is_admin:
        if status_filter:
            orders = order_crud.get_by_status(db, status=status_filter, skip=skip, limit=limit)
        else:
            orders = order_crud.get_multi(db, skip=skip, limit=limit)
    else:
        orders = order_crud.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get order by ID."""
    order = order_crud.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user has permission to view this order
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new order."""
    order = order_crud.create(db, user_id=current_user.id, order_in=order_in)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create order. Check product availability and stock."
        )
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order. Only admins can update status."""
    order = order_crud.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permissions
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Only admins can update status
    if order_in.status and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update order status"
        )
    
    updated_order = order_crud.update(db, order_id, order_in)
    return updated_order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel order."""
    order = order_crud.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permissions
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    cancelled_order = order_crud.cancel(db, order_id)
    if not cancelled_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled"
        )
    
    return cancelled_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Delete order (Admin only)."""
    success = order_crud.delete(db, order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return None

