from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.podcast import PodcastRead
from db import get_db
from models.podcast import Podcast as PodcastModel

router = APIRouter(prefix="/podcasts", tags=["podcasts"])

@router.get("", response_model=List[PodcastRead])
def list_podcasts(
    pastor: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(PodcastModel).filter(PodcastModel.is_active == True)
    if pastor:
        q = q.filter(PodcastModel.pastor_name == pastor)
    if category:
        q = q.filter(PodcastModel.category == category)
    return q.order_by(PodcastModel.release_date.desc()).all()

@router.get("/{podcast_id}", response_model=PodcastRead)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    p = db.query(PodcastModel).filter(PodcastModel.id == podcast_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return p
