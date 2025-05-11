from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from datetime import datetime
from db import Base

class Prayer(Base):
    __tablename__ = "prayers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prayer_text = Column(String, nullable=False)
    status = Column(String, default="Active")
    likes_count = Column(Integer, default=0)
    folded_hands_user_ids = Column(String, default="[]")
    heart_user_ids = Column(String, default="[]")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
