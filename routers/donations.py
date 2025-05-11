from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.donation import DonationCreate, DonationRead
from db import get_db
from models.donation import Donation as DonationModel
from dependencies import get_current_active_user

router = APIRouter(prefix="/donations", tags=["donations"])

@router.post("", response_model=DonationRead)
def create_donation(donation_in: DonationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    donation = DonationModel(
        user_id=current_user.id,
        amount=donation_in.amount,
        payment_method=donation_in.payment_method,
        purpose=donation_in.purpose
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

@router.get("", response_model=List[DonationRead])
def list_donations(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return db.query(DonationModel).filter(DonationModel.user_id==current_user.id).all()

@router.get("/{donation_id}", response_model=DonationRead)
def get_donation(donation_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    donation = db.query(DonationModel).filter(DonationModel.id==donation_id, DonationModel.user_id==current_user.id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Not found")
    return donation
