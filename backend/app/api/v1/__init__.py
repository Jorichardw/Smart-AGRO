"""
API v1 router initialization
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, farms, crops, weather, ai, iot, 
    marketplace, schemes, notifications, analytics
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["Users"]
)

api_router.include_router(
    farms.router, 
    prefix="/farms", 
    tags=["Farm Management"]
)

api_router.include_router(
    crops.router, 
    prefix="/crops", 
    tags=["Crop Management"]
)

api_router.include_router(
    weather.router, 
    prefix="/weather", 
    tags=["Weather Services"]
)

api_router.include_router(
    ai.router, 
    prefix="/ai", 
    tags=["AI Services"]
)

api_router.include_router(
    iot.router, 
    prefix="/iot", 
    tags=["IoT Dashboard"]
)

api_router.include_router(
    marketplace.router, 
    prefix="/marketplace", 
    tags=["Marketplace"]
)

api_router.include_router(
    schemes.router, 
    prefix="/schemes", 
    tags=["Government Schemes"]
)

api_router.include_router(
    notifications.router, 
    prefix="/notifications", 
    tags=["Notifications"]
)

api_router.include_router(
    analytics.router, 
    prefix="/analytics", 
    tags=["Analytics & Reports"]
)