from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.daily_verse import DailyVerseRead
from db import get_db
from models.daily_verse import DailyVerse as DVModel

router = APIRouter(prefix="/daily-verses", tags=["daily-verses"])

@router.get("", response_model=List[DailyVerseRead])
def list_daily_verses(db: Session = Depends(get_db)):
    return (
        db.query(DVModel)
        .filter(DVModel.is_active == True)
        .order_by(DVModel.display_date.desc())
        .all()
    )

@router.get("/{verse_id}", response_model=DailyVerseRead)
def get_daily_verse(verse_id: int, db: Session = Depends(get_db)):
    verse = db.query(DVModel).filter(DVModel.id == verse_id).first()
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse
