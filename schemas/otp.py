# schemas/otp.py

from pydantic import BaseModel

class OTPRequest(BaseModel):
    identifier: str  # phone number or email address

class OTPVerify(BaseModel):
    identifier: str
    code: str
