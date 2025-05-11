from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import Token, UserCreate, UserRead
from db import get_db
from models.user import User as UserModel
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserRead)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter((UserModel.email==user_in.email)|(UserModel.username==user_in.username)).first():
        raise HTTPException(status_code=400, detail="User exists")
    user = UserModel(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):  # reuse UserCreate for simplicity
    user = db.query(UserModel).filter(UserModel.username==form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def read_me(current_user = Depends(get_current_active_user)):
    return current_user
