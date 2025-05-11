from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DailyVerseRead(BaseModel):
    id: int
    title: str
    verse_text: str
    reflection: Optional[str]
    image_url: Optional[str]
    display_date: datetime

    model_config = ConfigDict(from_attributes=True)
