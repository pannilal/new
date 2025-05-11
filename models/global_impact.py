from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from db import Base

class GlobalImpact(Base):
    __tablename__ = "global_impact"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    name = Column(String, nullable=False)
    establishment_date = Column(DateTime, nullable=True)
    address = Column(String, nullable=True)
    main_pastor = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
