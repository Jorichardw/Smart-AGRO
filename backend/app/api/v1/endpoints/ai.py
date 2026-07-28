"""
AI endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.ai_service import AIService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/disease-detection")
async def detect_disease(
    image: UploadFile = File(...),
    crop_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Detect plant disease from image"""
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Check file size (max 10MB)
        contents = await image.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file too large (max 10MB)"
            )
        
        # Process with AI service
        ai_service = AIService(db)
        result = await ai_service.detect_disease(
            image_data=contents,
            crop_id=crop_id,
            user_id=str(current_user.id)
        )
        
        logger.info(f"Disease detection completed for user {current_user.email}")
        
        return {
            "status": "success",
            "filename": image.filename,
            "crop_id": crop_id,
            "detection_result": result,
            "user": current_user.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Disease detection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Disease detection failed. Please try again."
        )


@router.post("/pest-detection")
async def detect_pest(
    image: UploadFile = File(...),
    crop_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Detect pest from image"""
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Check file size (max 10MB)
        contents = await image.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file too large (max 10MB)"
            )
        
        # Process with AI service
        ai_service = AIService(db)
        result = await ai_service.detect_pest(
            image_data=contents,
            crop_id=crop_id,
            user_id=str(current_user.id)
        )
        
        logger.info(f"Pest detection completed for user {current_user.email}")
        
        return {
            "status": "success",
            "filename": image.filename,
            "crop_id": crop_id,
            "detection_result": result,
            "user": current_user.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pest detection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Pest detection failed. Please try again."
        )


@router.post("/crop-recommendations")
async def get_crop_recommendations(
    soil_data: Dict[str, Any],
    latitude: float,
    longitude: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get crop recommendations based on conditions"""
    try:
        # Get weather data for recommendations
        from app.services.weather_service import WeatherService
        weather_service = WeatherService(db)
        weather_data = await weather_service.get_current_weather(latitude, longitude)
        
        # Get AI recommendations
        ai_service = AIService(db)
        recommendations = await ai_service.get_crop_recommendations(
            soil_data=soil_data,
            weather_data=weather_data,
            location=(latitude, longitude)
        )
        
        return {
            "status": "success",
            "location": {"latitude": latitude, "longitude": longitude},
            "soil_conditions": soil_data,
            "recommendations": recommendations,
            "recommendation_count": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Crop recommendation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate crop recommendations"
        )


@router.get("/yield-prediction/{crop_id}")
async def predict_yield(
    crop_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Predict yield for specific crop"""
    try:
        # Verify crop ownership
        from app.services.farm_service import FarmService
        from app.services.farmer_service import FarmerService
        
        # Check if user has access to this crop
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Farmer profile required."
            )
        
        # Get yield prediction
        ai_service = AIService(db)
        prediction = await ai_service.predict_yield(crop_id)
        
        return {
            "status": "success",
            "crop_id": crop_id,
            "prediction": prediction
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Yield prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate yield prediction"
        )


@router.post("/chat")
async def chat_with_ai(
    message: str = Form(...),
    context: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Chat with AI assistant"""
    try:
        # Mock AI chat response for now
        responses = [
            f"Hello {current_user.first_name or 'there'}! I'm your AI farming assistant. How can I help you today?",
            "Based on current weather conditions, I recommend checking your crop irrigation schedule.",
            "For organic pest control, try neem oil or introducing beneficial insects like ladybugs.",
            "Your crops are looking healthy! Continue with your current care routine.",
            "I suggest soil testing every 6 months to maintain optimal nutrient levels."
        ]
        
        import random
        ai_response = random.choice(responses)
        
        # In production, this would call an actual AI chat service
        
        return {
            "status": "success",
            "user_message": message,
            "ai_response": ai_response,
            "context": context,
            "conversation_id": f"conv_{current_user.id}_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI assistant temporarily unavailable"
        )


# Import datetime for chat endpoint
from datetime import datetime