# routers/otp.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string
from core.config import settings
from db import get_db
from models.otp import OTP as OTPModel
from schemas.otp import OTPRequest, OTPVerify

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/request-otp")
def request_otp(
    data: OTPRequest,
    db: Session = Depends(get_db),
):
    # generate numeric OTP
    code = "".join(random.choices(string.digits, k=settings.OTP_LENGTH))
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

    otp = OTPModel(
        identifier=data.identifier,
        code=code,
        expires_at=expires_at,
    )
    db.add(otp)
    db.commit()

    # TODO: integrate your SMS/email send here
    return {
        "message": f"OTP sent to {data.identifier}",
        "expires_at": expires_at.isoformat(),
    }

@router.post("/verify-otp")
def verify_otp(
    data: OTPVerify,
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    otp = (
        db.query(OTPModel)
        .filter(
            OTPModel.identifier == data.identifier,
            OTPModel.code == data.code,
            OTPModel.is_used == False,
            OTPModel.expires_at >= now,
        )
        .order_by(OTPModel.created_at.desc())
        .first()
    )
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    otp.is_used = True
    db.commit()

    # TODO: Here you could auto-create/fetch the user and issue access/refresh tokens
    return {"message": "OTP verified successfully"}
