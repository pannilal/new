from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DonationCreate(BaseModel):
    amount: float
    payment_method: str
    purpose: Optional[str]

class DonationRead(DonationCreate):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
