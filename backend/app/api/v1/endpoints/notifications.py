"""
Notifications endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_notifications(current_user: User = Depends(get_current_user)):
    """Get user notifications - placeholder"""
    return {"message": "Notifications endpoint - Coming soon", "user": current_user.email}

@router.post("/{notification_id}/read")
async def mark_notification_read(notification_id: str, current_user: User = Depends(get_current_user)):
    """Mark notification as read - placeholder"""
    return {"message": "Mark notification read - Coming soon", "notification_id": notification_id}