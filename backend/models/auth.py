from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class FarmerRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr
    password: str = Field(..., min_length=6)
    state: str = Field(..., min_length=2)
    district: str = Field(..., min_length=2)
    farm_size: float = Field(..., gt=0.0, description="Farm size in hectares")


class FarmerLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordReset(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class UserResponse(BaseModel):
    uid: str
    name: str
    phone: str
    email: str
    state: str
    district: str
    farm_size: float
    role: str
