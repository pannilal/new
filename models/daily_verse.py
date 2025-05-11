from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from db import Base

class DailyVerse(Base):
    __tablename__ = "daily_verses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    verse_text = Column(String, nullable=False)
    reflection = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    display_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
