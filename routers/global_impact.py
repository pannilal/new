from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.global_impact import GlobalImpactRead
from db import get_db
from models.global_impact import GlobalImpact as GIModel

router = APIRouter(prefix="/global-impact", tags=["global-impact"])

@router.get("", response_model=List[GlobalImpactRead])
def list_global_impact(db: Session = Depends(get_db)):
    return (
        db.query(GIModel)
        .filter(GIModel.is_active == True)
        .order_by(GIModel.created_at.desc())
        .all()
    )

@router.get("/{gi_id}", response_model=GlobalImpactRead)
def get_global_impact(gi_id: int, db: Session = Depends(get_db)):
    gi = db.query(GIModel).filter(GIModel.id == gi_id).first()
    if not gi:
        raise HTTPException(status_code=404, detail="Global Impact not found")
    return gi
