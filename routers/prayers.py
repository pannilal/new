from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.prayer import PrayerCreate, PrayerRead
from db import get_db
from models.prayer import Prayer as PrayerModel
from dependencies import get_current_active_user

router = APIRouter(prefix="/prayers", tags=["prayers"])

@router.post("", response_model=PrayerRead)
def create_prayer(
    prayer_in: PrayerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    prayer = PrayerModel(user_id=current_user.id, prayer_text=prayer_in.prayer_text)
    db.add(prayer); db.commit(); db.refresh(prayer)
    return prayer

@router.get("", response_model=List[PrayerRead])
def list_prayers(db: Session = Depends(get_db)):
    return (
        db.query(PrayerModel)
        .filter(PrayerModel.is_active == True)
        .order_by(PrayerModel.created_at.desc())
        .all()
    )

@router.get("/me", response_model=List[PrayerRead])
def list_my_prayers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return (
        db.query(PrayerModel)
        .filter(PrayerModel.user_id == current_user.id)
        .order_by(PrayerModel.created_at.desc())
        .all()
    )

@router.get("/{prayer_id}", response_model=PrayerRead)
def get_prayer(prayer_id: int, db: Session = Depends(get_db)):
    prayer = (
        db.query(PrayerModel)
        .filter(PrayerModel.id == prayer_id, PrayerModel.is_active == True)
        .first()
    )
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    return prayer

@router.post("/{prayer_id}/react", response_model=PrayerRead)
def react_prayer(prayer_id: int, reaction: str, db: Session = Depends(get_db)):
    prayer = db.query(PrayerModel).filter(PrayerModel.id == prayer_id).first()
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    if reaction.lower() == "like":
        prayer.likes_count += 1
    elif reaction.lower() == "pray":
        # placeholder for folded_hands_user_ids logic
        prayer.folded_hands_user_ids = prayer.folded_hands_user_ids
    elif reaction.lower() == "heart":
        # placeholder for heart_user_ids logic
        prayer.heart_user_ids = prayer.heart_user_ids
    db.commit(); db.refresh(prayer)
    return prayer
