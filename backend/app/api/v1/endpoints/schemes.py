"""
Government Schemes endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_schemes(current_user: User = Depends(get_current_user)):
    """Get government schemes - placeholder"""
    return {"message": "Government schemes endpoint - Coming soon", "user": current_user.email}

@router.get("/applications")
async def get_applications(current_user: User = Depends(get_current_user)):
    """Get scheme applications - placeholder"""
    return {"message": "Scheme applications endpoint - Coming soon", "user": current_user.email}