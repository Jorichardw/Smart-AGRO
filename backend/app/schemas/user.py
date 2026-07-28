"""
User schemas for AGRO-BOT & AUTOMATION
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, validator

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.FARMER
    language_preference: Optional[str] = "en"


class UserCreate(UserBase):
    """User creation schema"""
    firebase_uid: str
    email: EmailStr
    first_name: str
    last_name: str
    
    @validator('firebase_uid')
    def validate_firebase_uid(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Firebase UID is required')
        return v.strip()
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v and len(v.strip()) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip() if v else v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Basic phone validation
            phone_digits = ''.join(filter(str.isdigit, v))
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class UserUpdate(BaseModel):
    """User update schema"""
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_preference: Optional[str] = None
    profile_image_url: Optional[str] = None
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v and len(v.strip()) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip() if v else v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            phone_digits = ''.join(filter(str.isdigit, v))
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class UserResponse(UserBase):
    """User response schema"""
    id: UUID
    firebase_uid: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True
    
    @validator('full_name', pre=True, always=True)
    def get_full_name(cls, v, values):
        if 'first_name' in values and 'last_name' in values:
            first = values.get('first_name', '') or ''
            last = values.get('last_name', '') or ''
            return f"{first} {last}".strip()
        return v


class UserList(BaseModel):
    """User list schema"""
    users: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class UserStats(BaseModel):
    """User statistics schema"""
    total_users: int
    active_users: int
    inactive_users: int
    farmers: int
    experts: int
    agriculture_officers: int
    admins: int


class UserSearch(BaseModel):
    """User search schema"""
    search_term: str
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    limit: Optional[int] = 10
    
    @validator('limit')
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError('Limit must be between 1 and 100')
        return v