from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.post import PostCreate, PostRead
from db import get_db
from models.post import SocialPost as PostModel
from dependencies import get_current_active_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostRead)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    post = PostModel(user_id=current_user.id, **post_in.dict())
    db.add(post); db.commit(); db.refresh(post)
    return post

@router.get("", response_model=List[PostRead])
def list_posts(db: Session = Depends(get_db)):
    return (
        db.query(PostModel)
        .filter(PostModel.status == "Active")
        .order_by(PostModel.created_at.desc())
        .all()
    )

@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = (
        db.query(PostModel)
        .filter(PostModel.id == post_id, PostModel.status == "Active")
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{post_id}/react", response_model=PostRead)
def react_post(post_id: int, reaction: str, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if reaction.lower() == "like":
        post.likes_count += 1
    elif reaction.lower() == "pray":
        post.folded_hands_count += 1
    elif reaction.lower() == "heart":
        post.heart_count += 1
    db.commit(); db.refresh(post)
    return post
