"""
Crop endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_crops(current_user: User = Depends(get_current_user)):
    """Get crops - placeholder endpoint"""
    return {"message": "Crop management endpoints - Coming soon", "user": current_user.email}

@router.get("/varieties")
async def get_crop_varieties():
    """Get crop varieties - placeholder"""
    return {"message": "Crop varieties endpoint - Coming soon"}