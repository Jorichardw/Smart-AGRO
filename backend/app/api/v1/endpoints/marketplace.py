"""
Marketplace endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/products")
async def get_products(current_user: User = Depends(get_current_user)):
    """Get marketplace products - placeholder"""
    return {"message": "Marketplace products endpoint - Coming soon", "user": current_user.email}

@router.get("/orders")
async def get_orders(current_user: User = Depends(get_current_user)):
    """Get marketplace orders - placeholder"""  
    return {"message": "Marketplace orders endpoint - Coming soon", "user": current_user.email}