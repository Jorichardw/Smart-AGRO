"""
AGRO-BOT & AUTOMATION - AI/ML Services API
Microservice for AI-powered agriculture features
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
from typing import Dict, Any, List, Optional
import time
import asyncio

from services.disease_detection import DiseaseDetectionService
from services.pest_detection import PestDetectionService
from services.yield_prediction import YieldPredictionService
from services.crop_recommendation import CropRecommendationService
from services.weather_prediction import WeatherPredictionService
from services.irrigation_optimization import IrrigationOptimizationService
from services.fertilizer_optimization import FertilizerOptimizationService
from services.soil_analysis import SoilAnalysisService
from services.chat_assistant import ChatAssistantService
from utils.logger import setup_logger
from utils.model_loader import ModelLoader
from utils.image_processor import ImageProcessor

# Setup logging
setup_logger()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AGRO-BOT AI Services",
    description="""
    **AI/ML Microservices for Smart Agriculture**
    
    This microservice provides AI-powered features for the AGRO-BOT platform:
    
    ## Features
    * 🦠 **Disease Detection** - Plant disease identification using computer vision
    * 🐛 **Pest Detection** - Pest identification and treatment recommendations
    * 📈 **Yield Prediction** - AI-based crop yield forecasting
    * 🌱 **Crop Recommendation** - Optimal crop suggestions based on conditions
    * 🌤️ **Weather Prediction** - Local weather forecasting
    * 💧 **Irrigation Optimization** - Smart water management recommendations
    * 🧪 **Fertilizer Optimization** - NPK recommendations based on soil and crop data
    * 🏔️ **Soil Analysis** - Soil health assessment and recommendations
    * 🤖 **Chat Assistant** - AI-powered farming advisor
    
    ## Models
    * YOLOv8 for object detection
    * ResNet/EfficientNet for image classification
    * LSTM/Transformer for time series prediction
    * Random Forest for structured data prediction
    * BERT/GPT for natural language processing
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORsMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for services
services = {}

@app.on_event("startup")
async def startup_event():
    """Initialize AI services on startup"""
    logger.info("Starting AGRO-BOT AI Services...")
    
    try:
        # Initialize model loader
        model_loader = ModelLoader()
        
        # Initialize services
        services['disease_detection'] = DiseaseDetectionService(model_loader)
        services['pest_detection'] = PestDetectionService(model_loader)
        services['yield_prediction'] = YieldPredictionService(model_loader)
        services['crop_recommendation'] = CropRecommendationService(model_loader)
        services['weather_prediction'] = WeatherPredictionService(model_loader)
        services['irrigation_optimization'] = IrrigationOptimizationService(model_loader)
        services['fertilizer_optimization'] = FertilizerOptimizationService(model_loader)
        services['soil_analysis'] = SoilAnalysisService(model_loader)
        services['chat_assistant'] = ChatAssistantService(model_loader)
        
        logger.info("AI Services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize AI services: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AGRO-BOT AI Services",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "Disease Detection",
            "Pest Detection", 
            "Yield Prediction",
            "Crop Recommendation",
            "Weather Prediction",
            "Irrigation Optimization",
            "Fertilizer Optimization",
            "Soil Analysis",
            "Chat Assistant"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services_loaded": len(services),
        "memory_usage": "TODO",  # Add actual memory usage
        "gpu_available": "TODO"   # Add GPU availability check
    }


# Disease Detection Endpoints
@app.post("/disease-detection/detect")
async def detect_disease(
    image: UploadFile = File(...),
    crop_type: Optional[str] = None,
    confidence_threshold: float = 0.7
):
    """
    Detect plant diseases from uploaded image
    
    Args:
        image: Plant image file
        crop_type: Type of crop (optional for better accuracy)
        confidence_threshold: Minimum confidence for detection
    
    Returns:
        Detection results with disease identification and recommendations
    """
    try:
        if 'disease_detection' not in services:
            raise HTTPException(status_code=503, detail="Disease detection service not available")
        
        # Process image
        image_processor = ImageProcessor()
        processed_image = await image_processor.process_upload(image)
        
        # Run detection
        result = await services['disease_detection'].detect(
            processed_image, 
            crop_type=crop_type,
            confidence_threshold=confidence_threshold
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Disease detection error: {e}")
        raise HTTPException(status_code=500, detail="Disease detection failed")


@app.post("/disease-detection/batch")
async def detect_diseases_batch(
    images: List[UploadFile] = File(...),
    crop_type: Optional[str] = None
):
    """Batch disease detection for multiple images"""
    try:
        if 'disease_detection' not in services:
            raise HTTPException(status_code=503, detail="Disease detection service not available")
        
        results = []
        image_processor = ImageProcessor()
        
        for image in images:
            processed_image = await image_processor.process_upload(image)
            result = await services['disease_detection'].detect(
                processed_image, 
                crop_type=crop_type
            )
            results.append(result)
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Batch disease detection error: {e}")
        raise HTTPException(status_code=500, detail="Batch detection failed")


# Pest Detection Endpoints
@app.post("/pest-detection/detect")
async def detect_pest(
    image: UploadFile = File(...),
    crop_type: Optional[str] = None,
    confidence_threshold: float = 0.6
):
    """
    Detect pests from uploaded image
    
    Args:
        image: Image containing pests
        crop_type: Type of crop (optional)
        confidence_threshold: Minimum confidence for detection
    
    Returns:
        Pest detection results with treatment recommendations
    """
    try:
        if 'pest_detection' not in services:
            raise HTTPException(status_code=503, detail="Pest detection service not available")
        
        image_processor = ImageProcessor()
        processed_image = await image_processor.process_upload(image)
        
        result = await services['pest_detection'].detect(
            processed_image,
            crop_type=crop_type,
            confidence_threshold=confidence_threshold
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Pest detection error: {e}")
        raise HTTPException(status_code=500, detail="Pest detection failed")


# Yield Prediction Endpoints
@app.post("/yield-prediction/predict")
async def predict_yield(
    crop_data: Dict[str, Any],
    weather_data: Optional[Dict[str, Any]] = None,
    soil_data: Optional[Dict[str, Any]] = None
):
    """
    Predict crop yield based on various factors
    
    Args:
        crop_data: Information about the crop (type, planting date, area, etc.)
        weather_data: Historical and current weather data
        soil_data: Soil analysis data
    
    Returns:
        Yield prediction with confidence intervals
    """
    try:
        if 'yield_prediction' not in services:
            raise HTTPException(status_code=503, detail="Yield prediction service not available")
        
        result = await services['yield_prediction'].predict(
            crop_data=crop_data,
            weather_data=weather_data,
            soil_data=soil_data
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Yield prediction error: {e}")
        raise HTTPException(status_code=500, detail="Yield prediction failed")


# Crop Recommendation Endpoints
@app.post("/crop-recommendation/recommend")
async def recommend_crops(
    location_data: Dict[str, Any],
    soil_data: Dict[str, Any],
    weather_data: Optional[Dict[str, Any]] = None,
    farmer_preferences: Optional[Dict[str, Any]] = None
):
    """
    Recommend optimal crops for given conditions
    
    Args:
        location_data: Geographic location and climate zone
        soil_data: Soil analysis results
        weather_data: Local weather patterns
        farmer_preferences: Farmer's preferences and constraints
    
    Returns:
        List of recommended crops with suitability scores
    """
    try:
        if 'crop_recommendation' not in services:
            raise HTTPException(status_code=503, detail="Crop recommendation service not available")
        
        result = await services['crop_recommendation'].recommend(
            location_data=location_data,
            soil_data=soil_data,
            weather_data=weather_data,
            farmer_preferences=farmer_preferences
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Crop recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Crop recommendation failed")


# Weather Prediction Endpoints
@app.post("/weather-prediction/forecast")
async def predict_weather(
    location: Dict[str, float],  # lat, lon
    days: int = 7,
    include_hourly: bool = False
):
    """
    Generate weather forecast for specific location
    
    Args:
        location: Latitude and longitude
        days: Number of days to forecast
        include_hourly: Include hourly forecasts
    
    Returns:
        Weather forecast with agricultural insights
    """
    try:
        if 'weather_prediction' not in services:
            raise HTTPException(status_code=503, detail="Weather prediction service not available")
        
        result = await services['weather_prediction'].forecast(
            location=location,
            days=days,
            include_hourly=include_hourly
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Weather prediction error: {e}")
        raise HTTPException(status_code=500, detail="Weather prediction failed")


# Irrigation Optimization Endpoints
@app.post("/irrigation/optimize")
async def optimize_irrigation(
    field_data: Dict[str, Any],
    crop_data: Dict[str, Any],
    weather_forecast: Dict[str, Any],
    sensor_data: Optional[Dict[str, Any]] = None
):
    """
    Optimize irrigation schedule and water usage
    
    Args:
        field_data: Field characteristics and soil data
        crop_data: Crop type and growth stage
        weather_forecast: Weather predictions
        sensor_data: Real-time sensor readings
    
    Returns:
        Optimized irrigation recommendations
    """
    try:
        if 'irrigation_optimization' not in services:
            raise HTTPException(status_code=503, detail="Irrigation optimization service not available")
        
        result = await services['irrigation_optimization'].optimize(
            field_data=field_data,
            crop_data=crop_data,
            weather_forecast=weather_forecast,
            sensor_data=sensor_data
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Irrigation optimization error: {e}")
        raise HTTPException(status_code=500, detail="Irrigation optimization failed")


# Fertilizer Optimization Endpoints
@app.post("/fertilizer/optimize")
async def optimize_fertilizer(
    crop_data: Dict[str, Any],
    soil_analysis: Dict[str, Any],
    target_yield: Optional[float] = None,
    budget_constraints: Optional[Dict[str, Any]] = None
):
    """
    Optimize fertilizer application for crops
    
    Args:
        crop_data: Crop information and growth stage
        soil_analysis: Current soil nutrient levels
        target_yield: Desired yield (optional)
        budget_constraints: Budget limitations
    
    Returns:
        Optimized fertilizer recommendations with NPK ratios
    """
    try:
        if 'fertilizer_optimization' not in services:
            raise HTTPException(status_code=503, detail="Fertilizer optimization service not available")
        
        result = await services['fertilizer_optimization'].optimize(
            crop_data=crop_data,
            soil_analysis=soil_analysis,
            target_yield=target_yield,
            budget_constraints=budget_constraints
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Fertilizer optimization error: {e}")
        raise HTTPException(status_code=500, detail="Fertilizer optimization failed")


# Soil Analysis Endpoints
@app.post("/soil-analysis/analyze")
async def analyze_soil(
    soil_image: Optional[UploadFile] = File(None),
    lab_results: Optional[Dict[str, Any]] = None,
    location: Optional[Dict[str, float]] = None
):
    """
    Analyze soil health and provide recommendations
    
    Args:
        soil_image: Image of soil sample (optional)
        lab_results: Laboratory soil test results
        location: Geographic coordinates for regional insights
    
    Returns:
        Soil health analysis and improvement recommendations
    """
    try:
        if 'soil_analysis' not in services:
            raise HTTPException(status_code=503, detail="Soil analysis service not available")
        
        processed_image = None
        if soil_image:
            image_processor = ImageProcessor()
            processed_image = await image_processor.process_upload(soil_image)
        
        result = await services['soil_analysis'].analyze(
            soil_image=processed_image,
            lab_results=lab_results,
            location=location
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Soil analysis error: {e}")
        raise HTTPException(status_code=500, detail="Soil analysis failed")


# Chat Assistant Endpoints
@app.post("/chat/query")
async def chat_query(
    message: str,
    context: Optional[Dict[str, Any]] = None,
    language: str = "en",
    include_voice: bool = False
):
    """
    Process farmer's query through AI chat assistant
    
    Args:
        message: Farmer's question or message
        context: Additional context (farm, crop, location data)
        language: Language code for response
        include_voice: Generate voice response
    
    Returns:
        AI assistant response with recommendations
    """
    try:
        if 'chat_assistant' not in services:
            raise HTTPException(status_code=503, detail="Chat assistant service not available")
        
        result = await services['chat_assistant'].process_query(
            message=message,
            context=context,
            language=language,
            include_voice=include_voice
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Chat query error: {e}")
        raise HTTPException(status_code=500, detail="Chat query failed")


@app.post("/chat/voice")
async def process_voice_input(
    audio: UploadFile = File(...),
    language: str = "en",
    context: Optional[Dict[str, Any]] = None
):
    """
    Process voice input from farmer
    
    Args:
        audio: Audio file with farmer's voice input
        language: Language code for speech recognition
        context: Additional context for better understanding
    
    Returns:
        Transcribed text and AI response
    """
    try:
        if 'chat_assistant' not in services:
            raise HTTPException(status_code=503, detail="Chat assistant service not available")
        
        result = await services['chat_assistant'].process_voice_input(
            audio_file=audio,
            language=language,
            context=context
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        raise HTTPException(status_code=500, detail="Voice processing failed")


# Model Management Endpoints
@app.get("/models/status")
async def get_model_status():
    """Get status of all loaded AI models"""
    try:
        status = {}
        for service_name, service in services.items():
            if hasattr(service, 'get_model_info'):
                status[service_name] = await service.get_model_info()
            else:
                status[service_name] = {"loaded": True}
        
        return {"models": status}
        
    except Exception as e:
        logger.error(f"Model status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model status")


@app.post("/models/reload")
async def reload_models(background_tasks: BackgroundTasks):
    """Reload all AI models"""
    try:
        background_tasks.add_task(reload_all_models)
        return {"message": "Model reload initiated"}
        
    except Exception as e:
        logger.error(f"Model reload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload models")


async def reload_all_models():
    """Background task to reload all models"""
    logger.info("Reloading all AI models...")
    try:
        # Reinitialize services
        global services
        model_loader = ModelLoader()
        
        for service_name in services.keys():
            if service_name == 'disease_detection':
                services[service_name] = DiseaseDetectionService(model_loader)
            elif service_name == 'pest_detection':
                services[service_name] = PestDetectionService(model_loader)
            # Add other services as needed
        
        logger.info("All models reloaded successfully")
        
    except Exception as e:
        logger.error(f"Model reload failed: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )