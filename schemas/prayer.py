from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class PrayerCreate(BaseModel):
    prayer_text: str

class PrayerRead(BaseModel):
    id: int
    user_id: int
    prayer_text: str
    status: str
    likes_count: int
    folded_hands_user_ids: List[int]
    heart_user_ids: List[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
