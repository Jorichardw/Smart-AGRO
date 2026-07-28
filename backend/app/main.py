"""
AGRO-BOT & AUTOMATION - Main FastAPI Application
Smart Agriculture Platform Backend
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
import os
from typing import Dict, Any

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.core.security import get_current_user
from app.api.v1 import api_router
from app.models import Base
from app.services.firebase_service import FirebaseService
from app.utils.logger import setup_logger

# Setup logging
setup_logger()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AGRO-BOT & AUTOMATION API...")
    
    # Initialize Firebase
    try:
        firebase_service = FirebaseService()
        app.state.firebase = firebase_service
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    logger.info("API startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AGRO-BOT & AUTOMATION API...")


# Create FastAPI app
app = FastAPI(
    title="AGRO-BOT & AUTOMATION API",
    description="""
    **AI-Powered Smart Agriculture Platform**
    
    A comprehensive backend API for smart farming that provides:
    
    ## Features
    * 🌱 **Crop Management** - Complete farm and crop lifecycle tracking
    * 🦠 **Disease Detection** - AI-powered plant disease identification
    * 🌡️ **Weather Monitoring** - Real-time weather data and forecasting
    * 💧 **Smart Irrigation** - IoT-based automated irrigation system
    * 🧪 **Soil Analysis** - NPK levels and soil health monitoring
    * 🐛 **Pest Detection** - AI-based pest identification
    * 🤖 **AI Assistant** - Voice-enabled farming advisor
    * 📊 **IoT Dashboard** - Real-time sensor data visualization
    * 🛒 **Marketplace** - Agricultural e-commerce platform
    * 🏛️ **Government Schemes** - Subsidies and loan information
    
    ## Authentication
    Uses Firebase Authentication with JWT tokens.
    
    ## Rate Limiting
    API endpoints are rate-limited for fair usage.
    """,
    version="1.0.0",
    contact={
        "name": "AGRO-BOT Support",
        "email": "support@agro-bot.com",
        "url": "https://agro-bot.com/contact"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate response time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(
        f"Response: {response.status_code} | "
        f"Time: {process_time:.4f}s | "
        f"Path: {request.url.path}"
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error occurred",
            "status_code": 500
        }
    )


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """System health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "database": "connected",  # TODO: Add actual DB health check
        "redis": "connected",     # TODO: Add actual Redis health check
        "firebase": "connected"   # TODO: Add actual Firebase health check
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to AGRO-BOT & AUTOMATION API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include API router
app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)


# API Info endpoint
@app.get("/api/info", tags=["System"])
async def api_info():
    """Get API information and statistics"""
    return {
        "name": "AGRO-BOT & AUTOMATION API",
        "version": "1.0.0",
        "description": "AI-Powered Smart Agriculture Platform",
        "environment": settings.ENVIRONMENT,
        "features": [
            "Crop Management",
            "Disease Detection", 
            "Weather Monitoring",
            "Smart Irrigation",
            "Soil Analysis",
            "Pest Detection",
            "AI Assistant",
            "IoT Dashboard",
            "Marketplace",
            "Government Schemes"
        ],
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "farms": "/api/v1/farms",
            "crops": "/api/v1/crops",
            "weather": "/api/v1/weather",
            "ai": "/api/v1/ai",
            "iot": "/api/v1/iot",
            "marketplace": "/api/v1/marketplace",
            "schemes": "/api/v1/schemes"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )