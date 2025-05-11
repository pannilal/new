from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EventRead(BaseModel):
    id: int
    title: str
    category: Optional[str]
    image_url: Optional[str]
    event_date: datetime
    description: Optional[str]
    organizer: Optional[str]

    model_config = ConfigDict(from_attributes=True)
