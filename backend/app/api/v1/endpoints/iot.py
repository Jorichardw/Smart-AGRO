"""
IoT endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends
from typing import List, Optional
from uuid import UUID

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/devices")
async def get_devices(current_user: User = Depends(get_current_user)):
    """Get IoT devices - placeholder"""
    return {"message": "IoT devices endpoint - Coming soon", "user": current_user.email}

@router.get("/devices/{device_id}/readings")
async def get_device_readings(
    device_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get sensor readings from device - placeholder"""
    return {
        "message": "Device readings endpoint - Coming soon",
        "device_id": str(device_id),
        "user": current_user.email
    }

@router.post("/devices/{device_id}/readings")
async def submit_sensor_reading(
    device_id: UUID,
    reading_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Submit sensor reading - placeholder"""
    return {
        "message": "Sensor reading submitted - Coming soon",
        "device_id": str(device_id),
        "data": reading_data,
        "user": current_user.email
    }