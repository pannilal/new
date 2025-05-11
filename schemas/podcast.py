from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PodcastRead(BaseModel):
    id: int
    title: str
    category: Optional[str]
    pastor_name: Optional[str]
    media_url: str
    thumbnail_url: Optional[str]
    description: Optional[str]
    release_date: datetime

    model_config = ConfigDict(from_attributes=True)
