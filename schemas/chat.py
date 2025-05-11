from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ChatRoomCreate(BaseModel):
    user2_id: int

class ChatRoomRead(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatMessageCreate(BaseModel):
    message_text: Optional[str]
    media_url: Optional[str]
    media_type: Optional[str]

class ChatMessageRead(BaseModel):
    id: int
    chat_room_id: int
    sender_id: int
    message_text: Optional[str]
    media_url: Optional[str]
    media_type: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
