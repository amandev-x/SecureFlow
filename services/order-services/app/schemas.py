from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int 
    user_id: int 
    product_id: int
    quantity: int 
    total_price: float
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}

