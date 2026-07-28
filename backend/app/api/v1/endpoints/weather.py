"""
Weather endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.weather_service import WeatherService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/current")
async def get_current_weather(
    latitude: float = Query(..., description="Latitude", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude", ge=-180, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get current weather for location"""
    try:
        weather_service = WeatherService(db)
        weather_data = await weather_service.get_current_weather(latitude, longitude)
        
        logger.info(f"Weather requested by {current_user.email} for {latitude}, {longitude}")
        
        return {
            "status": "success",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "weather": weather_data,
            "timestamp": weather_data.get("timestamp")
        }
        
    except Exception as e:
        logger.error(f"Error getting current weather: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch weather data"
        )


@router.get("/forecast")
async def get_weather_forecast(
    latitude: float = Query(..., description="Latitude", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude", ge=-180, le=180),
    days: Optional[int] = Query(7, ge=1, le=14, description="Number of forecast days"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get weather forecast for location"""
    try:
        weather_service = WeatherService(db)
        forecast_data = await weather_service.get_weather_forecast(latitude, longitude, days)
        
        logger.info(f"Weather forecast requested by {current_user.email} for {latitude}, {longitude}")
        
        return {
            "status": "success",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "forecast_days": days,
            "forecast": forecast_data
        }
        
    except Exception as e:
        logger.error(f"Error getting weather forecast: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch weather forecast"
        )


@router.get("/alerts")
async def get_weather_alerts(
    latitude: float = Query(..., description="Latitude", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude", ge=-180, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get weather alerts for location"""
    try:
        weather_service = WeatherService(db)
        alerts = await weather_service.get_weather_alerts(latitude, longitude)
        
        return {
            "status": "success",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "alerts": alerts,
            "alert_count": len(alerts)
        }
        
    except Exception as e:
        logger.error(f"Error getting weather alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch weather alerts"
        )


@router.get("/history")
async def get_weather_history(
    latitude: float = Query(..., description="Latitude", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude", ge=-180, le=180),
    days_back: Optional[int] = Query(30, ge=1, le=90, description="Number of days back"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get historical weather data"""
    try:
        weather_service = WeatherService(db)
        history_data = weather_service.get_weather_history(latitude, longitude, days_back)
        
        return {
            "status": "success",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "days_back": days_back,
            "history": history_data,
            "data_points": len(history_data)
        }
        
    except Exception as e:
        logger.error(f"Error getting weather history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch weather history"
        )