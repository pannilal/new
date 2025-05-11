from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.chat import ChatRoomCreate, ChatRoomRead, ChatMessageCreate, ChatMessageRead
from db import get_db
from models.chat_room import ChatRoom as ChatRoomModel
from models.chat_message import ChatMessage as ChatMessageModel
from dependencies import get_current_active_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/rooms", response_model=ChatRoomRead)
def create_chat_room(
    room_in: ChatRoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    room = ChatRoomModel(user1_id=current_user.id, user2_id=room_in.user2_id)
    db.add(room); db.commit(); db.refresh(room)
    return room

@router.get("/rooms", response_model=List[ChatRoomRead])
def list_chat_rooms(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return db.query(ChatRoomModel).filter(
        (ChatRoomModel.user1_id == current_user.id)
        | (ChatRoomModel.user2_id == current_user.id)
    ).all()

@router.get("/rooms/{room_id}/messages", response_model=List[ChatMessageRead])
def list_chat_messages(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    # (optionally check membership)
    return (
        db.query(ChatMessageModel)
        .filter(ChatMessageModel.chat_room_id == room_id)
        .order_by(ChatMessageModel.created_at)
        .all()
    )

@router.post("/rooms/{room_id}/messages", response_model=ChatMessageRead)
def send_message(
    room_id: int,
    msg_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    message = ChatMessageModel(
        chat_room_id=room_id,
        sender_id=current_user.id,
        message_text=msg_in.message_text,
        media_url=msg_in.media_url,
        media_type=msg_in.media_type,
    )
    db.add(message); db.commit(); db.refresh(message)
    return message
