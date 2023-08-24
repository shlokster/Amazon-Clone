from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class OrderEntity(BaseModel):
    product_id: int
    supplier_id: int
    quantity: int
    price: int
class OrderDetails(BaseModel):
    id: int
    user_id: int
    total_price: int
    created_at: datetime
    order_entities: list[OrderEntity]


