from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CustomerCreatedPayload(BaseModel):
    user_id: str
    created_at: datetime


class OrderCompletedPayload(BaseModel):
    user_id: str
    total_price: float
    created_at: datetime


class TransactionCreatedPayload(BaseModel):
    user_id: str
    amount: float
    type: Literal["TRANSFER", "PURCHASE"]
    created_at: datetime


class ProductMovementPayload(BaseModel):
    product_id: str
    quantity: int
    movement_type: Literal["SOLD", "PURCHASED"]
    created_at: datetime
