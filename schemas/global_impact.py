from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class GlobalImpactRead(BaseModel):
    id: int
    country: str
    name: str
    establishment_date: Optional[datetime]
    address: Optional[str]
    main_pastor: Optional[str]
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)
