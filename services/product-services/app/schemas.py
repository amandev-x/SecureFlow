from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}