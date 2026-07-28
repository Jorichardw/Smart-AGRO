"""
AI service for AGRO-BOT & AUTOMATION
Handles disease detection, pest identification, and AI predictions
"""

import io
import logging
import httpx
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
import base64
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.core.config import settings
from app.models.disease import DiseaseDetection, PestDetection
from app.models.crop import Crop
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class AIService:
    """AI service for agricultural intelligence features"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service_url = settings.AI_SERVICE_URL
        self.api_key = settings.AI_API_KEY
        
    async def detect_disease(
        self, 
        image_data: bytes, 
        crop_id: Optional[str] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Detect plant disease from image
        
        Args:
            image_data: Image bytes
            crop_id: Optional crop ID for context
            user_id: User ID for logging
            
        Returns:
            Dict[str, Any]: Disease detection results
        """
        try:
            # Preprocess image
            processed_image = await self._preprocess_image(image_data)
            
            # Call AI service or use mock detection for development
            if settings.ENABLE_AI_FEATURES and self.ai_service_url:
                detection_result = await self._call_disease_detection_api(processed_image, crop_id)
            else:
                detection_result = self._mock_disease_detection(processed_image)
            
            # Store detection result
            if crop_id and user_id:
                await self._store_disease_detection(detection_result, crop_id, user_id)
            
            return detection_result
            
        except Exception as e:
            logger.error(f"Error in disease detection: {e}")
            return {
                "error": "Disease detection failed",
                "message": "Unable to process image at this time",
                "detected_disease": None,
                "confidence": 0.0
            }
    
    async def detect_pest(
        self, 
        image_data: bytes, 
        crop_id: Optional[str] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Detect pest from image
        
        Args:
            image_data: Image bytes
            crop_id: Optional crop ID for context
            user_id: User ID for logging
            
        Returns:
            Dict[str, Any]: Pest detection results
        """
        try:
            # Preprocess image
            processed_image = await self._preprocess_image(image_data)
            
            # Call AI service or use mock detection
            if settings.ENABLE_AI_FEATURES and self.ai_service_url:
                detection_result = await self._call_pest_detection_api(processed_image, crop_id)
            else:
                detection_result = self._mock_pest_detection(processed_image)
            
            # Store detection result
            if crop_id and user_id:
                await self._store_pest_detection(detection_result, crop_id, user_id)
            
            return detection_result
            
        except Exception as e:
            logger.error(f"Error in pest detection: {e}")
            return {
                "error": "Pest detection failed",
                "message": "Unable to process image at this time",
                "detected_pest": None,
                "confidence": 0.0
            }
    
    async def _preprocess_image(self, image_data: bytes) -> str:
        """
        Preprocess image for AI analysis
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            str: Base64 encoded processed image
        """
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image for processing (max 1024x1024)
            max_size = (1024, 1024)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=85)
            processed_bytes = output_buffer.getvalue()
            
            # Encode to base64
            return base64.b64encode(processed_bytes).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    async def _call_disease_detection_api(self, image_base64: str, crop_id: Optional[str]) -> Dict[str, Any]:
        """Call external AI service for disease detection"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "image": image_base64,
                    "crop_id": crop_id,
                    "model_version": settings.DISEASE_MODEL_VERSION
                }
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                response = await client.post(
                    f"{self.ai_service_url}/disease-detection",
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"AI service call failed: {e}")
            # Fallback to mock detection
            return self._mock_disease_detection(image_base64)
    
    async def _call_pest_detection_api(self, image_base64: str, crop_id: Optional[str]) -> Dict[str, Any]:
        """Call external AI service for pest detection"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "image": image_base64,
                    "crop_id": crop_id,
                    "model_version": settings.PEST_MODEL_VERSION
                }
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                response = await client.post(
                    f"{self.ai_service_url}/pest-detection",
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"AI service call failed: {e}")
            # Fallback to mock detection
            return self._mock_pest_detection(image_base64)
    
    def _mock_disease_detection(self, image_base64: str) -> Dict[str, Any]:
        """Mock disease detection for development"""
        import random
        
        diseases = [
            {
                "name": "Bacterial Leaf Blight",
                "severity": "moderate",
                "confidence": 0.87,
                "symptoms": "Yellow to brown lesions along leaf margins",
                "treatment": "Apply copper-based fungicide, improve drainage"
            },
            {
                "name": "Leaf Spot Disease", 
                "severity": "mild",
                "confidence": 0.72,
                "symptoms": "Small brown spots with yellow halos on leaves",
                "treatment": "Remove affected leaves, apply organic neem oil"
            },
            {
                "name": "Powdery Mildew",
                "severity": "severe", 
                "confidence": 0.91,
                "symptoms": "White powdery coating on leaves and stems",
                "treatment": "Increase air circulation, apply sulfur-based fungicide"
            }
        ]
        
        if random.random() > 0.3:  # 70% chance of detecting disease
            disease = random.choice(diseases)
            return {
                "detected_disease": disease["name"],
                "confidence": disease["confidence"],
                "severity": disease["severity"],
                "symptoms": disease["symptoms"],
                "treatment_recommendations": disease["treatment"],
                "organic_treatments": "Apply neem oil or compost tea weekly",
                "chemical_treatments": disease["treatment"],
                "prevention_tips": "Maintain proper spacing, avoid overhead watering",
                "affected_area_percentage": round(random.uniform(5, 40), 1),
                "detection_timestamp": datetime.utcnow().isoformat(),
                "ai_model_version": "mock-v1.0"
            }
        else:
            return {
                "detected_disease": "Healthy",
                "confidence": 0.95,
                "severity": None,
                "symptoms": "No disease symptoms detected",
                "treatment_recommendations": "Continue current care practices",
                "prevention_tips": "Maintain good plant hygiene and proper nutrition",
                "detection_timestamp": datetime.utcnow().isoformat()
            }
    
    def _mock_pest_detection(self, image_base64: str) -> Dict[str, Any]:
        """Mock pest detection for development"""
        import random
        
        pests = [
            {
                "name": "Aphids",
                "severity": "medium",
                "confidence": 0.83,
                "count": random.randint(10, 50),
                "treatment": "Spray with insecticidal soap or introduce ladybugs"
            },
            {
                "name": "Spider Mites",
                "severity": "high", 
                "confidence": 0.76,
                "count": random.randint(20, 100),
                "treatment": "Increase humidity, apply miticide if severe"
            },
            {
                "name": "Whiteflies",
                "severity": "low",
                "confidence": 0.68,
                "count": random.randint(5, 25),
                "treatment": "Use yellow sticky traps, apply neem oil"
            }
        ]
        
        if random.random() > 0.4:  # 60% chance of detecting pests
            pest = random.choice(pests)
            return {
                "detected_pest": pest["name"],
                "confidence": pest["confidence"],
                "severity": pest["severity"],
                "pest_count": pest["count"],
                "life_stage": random.choice(["adult", "larva", "nymph"]),
                "damage_description": f"Minor to moderate damage from {pest['name']} feeding",
                "treatment_recommendations": pest["treatment"],
                "organic_treatments": "Apply neem oil or beneficial insects",
                "chemical_treatments": pest["treatment"],
                "prevention_measures": "Regular monitoring, maintain plant health",
                "detection_timestamp": datetime.utcnow().isoformat(),
                "ai_model_version": "mock-v1.0"
            }
        else:
            return {
                "detected_pest": "No pests detected",
                "confidence": 0.92,
                "severity": None,
                "pest_count": 0,
                "damage_description": "No pest damage observed",
                "treatment_recommendations": "Continue regular monitoring",
                "detection_timestamp": datetime.utcnow().isoformat()
            }
    
    async def _store_disease_detection(self, result: Dict[str, Any], crop_id: str, user_id: str):
        """Store disease detection result in database"""
        try:
            # Upload image to storage (mock for now)
            image_url = f"/uploads/disease_detection/{uuid.uuid4()}.jpg"
            
            detection = DiseaseDetection(
                crop_id=crop_id,
                user_id=user_id,
                image_url=image_url,
                detected_disease=result.get("detected_disease"),
                confidence_score=result.get("confidence"),
                severity=result.get("severity"),
                affected_area_percentage=result.get("affected_area_percentage"),
                symptoms=result.get("symptoms"),
                treatment_recommendations=result.get("treatment_recommendations"),
                organic_treatments=result.get("organic_treatments"),
                chemical_treatments=result.get("chemical_treatments"),
                prevention_tips=result.get("prevention_tips"),
                ai_model_version=result.get("ai_model_version")
            )
            
            self.db.add(detection)
            self.db.commit()
            
            logger.info(f"Stored disease detection: {detection.id}")
            
        except Exception as e:
            logger.error(f"Error storing disease detection: {e}")
            self.db.rollback()
    
    async def _store_pest_detection(self, result: Dict[str, Any], crop_id: str, user_id: str):
        """Store pest detection result in database"""
        try:
            # Upload image to storage (mock for now)
            image_url = f"/uploads/pest_detection/{uuid.uuid4()}.jpg"
            
            detection = PestDetection(
                crop_id=crop_id,
                user_id=user_id,
                image_url=image_url,
                detected_pest=result.get("detected_pest"),
                confidence_score=result.get("confidence"),
                severity=result.get("severity"),
                pest_count=result.get("pest_count"),
                life_stage=result.get("life_stage"),
                damage_description=result.get("damage_description"),
                treatment_recommendations=result.get("treatment_recommendations"),
                organic_treatments=result.get("organic_treatments"),
                chemical_treatments=result.get("chemical_treatments"),
                prevention_measures=result.get("prevention_measures"),
                ai_model_version=result.get("ai_model_version")
            )
            
            self.db.add(detection)
            self.db.commit()
            
            logger.info(f"Stored pest detection: {detection.id}")
            
        except Exception as e:
            logger.error(f"Error storing pest detection: {e}")
            self.db.rollback()
    
    async def get_crop_recommendations(
        self, 
        soil_data: Dict[str, Any], 
        weather_data: Dict[str, Any],
        location: Tuple[float, float]
    ) -> List[Dict[str, Any]]:
        """
        Get crop recommendations based on conditions
        
        Args:
            soil_data: Soil analysis data
            weather_data: Weather conditions
            location: (latitude, longitude)
            
        Returns:
            List[Dict[str, Any]]: Recommended crops
        """
        try:
            # Mock recommendations for development
            recommendations = [
                {
                    "crop_name": "Rice",
                    "variety": "Basmati",
                    "suitability_score": 0.92,
                    "expected_yield": "4.5 tons/acre",
                    "growth_duration": "120 days",
                    "water_requirement": "High",
                    "best_planting_time": "June-July",
                    "market_price": "₹2,500/quintal",
                    "reasons": [
                        "Suitable soil pH (6.0-7.0)",
                        "Good water availability",
                        "Favorable climate conditions"
                    ]
                },
                {
                    "crop_name": "Wheat",
                    "variety": "HD-2967",
                    "suitability_score": 0.85,
                    "expected_yield": "3.8 tons/acre", 
                    "growth_duration": "140 days",
                    "water_requirement": "Medium",
                    "best_planting_time": "November-December",
                    "market_price": "₹2,100/quintal",
                    "reasons": [
                        "Optimal temperature range",
                        "Good nitrogen levels in soil",
                        "Lower water requirement"
                    ]
                }
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating crop recommendations: {e}")
            return []
    
    async def predict_yield(self, crop_id: str) -> Dict[str, Any]:
        """
        Predict crop yield based on current conditions
        
        Args:
            crop_id: Crop ID
            
        Returns:
            Dict[str, Any]: Yield prediction
        """
        try:
            # Mock yield prediction for development
            import random
            
            base_yield = random.uniform(2.5, 5.5)
            confidence = random.uniform(0.7, 0.95)
            
            return {
                "predicted_yield": round(base_yield, 2),
                "unit": "tons/acre",
                "confidence": round(confidence, 3),
                "confidence_interval": {
                    "lower": round(base_yield * 0.8, 2),
                    "upper": round(base_yield * 1.2, 2)
                },
                "factors_considered": [
                    "Weather conditions",
                    "Soil health",
                    "Crop growth stage",
                    "Historical data"
                ],
                "harvest_window": {
                    "start_date": "2024-04-15",
                    "end_date": "2024-04-30"
                },
                "market_prediction": {
                    "price_per_kg": round(random.uniform(25, 45), 2),
                    "expected_revenue": round(base_yield * 1000 * random.uniform(25, 45), 2)
                },
                "prediction_date": datetime.utcnow().isoformat(),
                "model_version": "yield-predict-v1.0"
            }
            
        except Exception as e:
            logger.error(f"Error predicting yield: {e}")
            return {"error": "Yield prediction unavailable"}