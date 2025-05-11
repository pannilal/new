from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.event import EventRead
from db import get_db
from models.event import Event as EventModel

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[EventRead])
def list_events(
    type: Optional[str] = Query(None, description="upcoming|past"),
    db: Session = Depends(get_db),
):
    q = db.query(EventModel).filter(EventModel.is_active == True)
    if type == "upcoming":
        q = q.filter(EventModel.event_date >= func.now())
    elif type == "past":
        q = q.filter(EventModel.event_date < func.now())
    return q.order_by(EventModel.event_date.desc()).all()

@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
