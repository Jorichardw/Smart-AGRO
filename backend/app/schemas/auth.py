"""
Authentication schemas for AGRO-BOT & AUTOMATION
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    firebase_id_token: str = Field(..., description="Firebase ID token")
    
    @validator('firebase_id_token')
    def validate_token(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Firebase ID token is required')
        return v.strip()


class FarmerRegisterData(BaseModel):
    farmer_id: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    total_land_area: Optional[float] = None
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    annual_income: Optional[float] = None
    
    @validator('total_land_area')
    def validate_land_area(cls, v):
        if v is not None and v < 0:
            raise ValueError('Land area cannot be negative')
        return v
    
    @validator('experience_years')
    def validate_experience(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Experience must be between 0 and 100 years')
        return v


class UserRegister(BaseModel):
    firebase_id_token: str = Field(..., description="Firebase ID token")
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field("farmer", description="User role")
    language_preference: Optional[str] = Field("en", description="Language preference")
    farmer_data: Optional[FarmerRegisterData] = None
    
    @validator('firebase_id_token')
    def validate_token(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Firebase ID token is required')
        return v.strip()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            phone_digits = ''.join(filter(str.isdigit, v))
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    firebase_uid: str
    email: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    profile_image_url: Optional[str] = None
    language_preference: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    message: str = "Login successful"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr