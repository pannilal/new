from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class PostCreate(BaseModel):
    text_content: Optional[str]
    media_url: Optional[str]
    media_type: Optional[str]
    location: Optional[str]
    tags: Optional[str]

class PostRead(BaseModel):
    id: int
    user_id: int
    text_content: Optional[str]
    media_url: Optional[str]
    media_type: Optional[str]
    location: Optional[str]
    tags: Optional[str]
    likes_count: int
    folded_hands_count: int
    heart_count: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
