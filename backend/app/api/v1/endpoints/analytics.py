"""
Analytics endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_data(current_user: User = Depends(get_current_user)):
    """Get dashboard analytics - placeholder"""
    return {"message": "Dashboard analytics endpoint - Coming soon", "user": current_user.email}

@router.get("/reports")
async def get_reports(current_user: User = Depends(get_admin_user)):
    """Get analytics reports - placeholder"""
    return {"message": "Analytics reports endpoint - Coming soon", "user": current_user.email}