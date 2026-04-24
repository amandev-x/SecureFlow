import os 
import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session 
from typing import List
from jose import jwt, JWTError

from app.database import get_db
from app.models import Order, OrderStatus
from app.schemas import OrderCreate, OrderResponse
from app.services.product_client import get_product

router = APIRouter(prefix="/orders", tags=["orders"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8004")


def get_user_id_from_token(authorization: str = Header(...)) -> int:
    """Extract user id from Bearer token passed in Authorization header"""
    try:
        parts = authorization.strip().split()

        if len(parts) == 2:
            scheme, token = parts
            
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                    )
        elif len(parts) == 1:
            token = parts[0]

        else:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user_id = payload.get("user_id")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="user_id missing from token")
        
        return {"user_id": user_id, "email": email}
    
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )
    

async def notify_order_confirmed(user_email: str, order_id: int, total_price: float):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"{NOTIFICATION_SERVICE_URL}/notify/order-confirmed",
                params={"user_email": user_email, "order_id": order_id, "total_price": total_price},timeout=5
            )
        
        except Exception:
            pass

async def notify_order_cancelled(user_email: str, order_id: int, total_price: float):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"{NOTIFICATION_SERVICE_URL}/notify/order-cancelled",
                params={"user_email": user_email, "order_id": order_id},
                timeout=5
            )
        
        except Exception:
            pass

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_user_id_from_token)):


    product = await get_product(order.product_id)

    if not product.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available"
        )
    
    if product["stock"] < order.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product['stock']}"
        )
    
    total_price = product["price"] * order.quantity

    new_order = Order(
        user_id=user["user_id"],
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status=OrderStatus.pending
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

    await notify_order_confirmed(
        user_email=user["email"],
        order_id=new_order.id,
        total_price=new_order.total_price
    )

    return new_order

@router.get("/", response_model=List[OrderResponse])
async def list_orders(db: Session = Depends(get_db), user: dict = Depends(get_user_id_from_token)):
    return db.query(Order).filter(Order.user_id == user["user_id"]).all()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user_id_from_token)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user["user_id"]).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return order 

@router.patch("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user_id_from_token)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user["user_id"]).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    if order.status == OrderStatus.cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already cancelled"
        )
    
    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)

    await notify_order_cancelled(user["email"], order.id, order.total_price)

    return order 


        





