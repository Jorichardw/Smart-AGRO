"""
Configuration settings for AGRO-BOT & AUTOMATION API
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import validator
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Basic Configuration
    PROJECT_NAME: str = "AGRO-BOT & AUTOMATION"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Smart Agriculture Platform"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "agro-bot-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://agro-bot.com",
        "https://app.agro-bot.com",
        "https://admin.agro-bot.com"
    ]
    
    # Allowed hosts for production
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "agro-bot.com",
        "api.agro-bot.com"
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://agro_user:agro_password@localhost:5432/agro_bot_db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID: str = "agro-bot-automation"
    FIREBASE_PRIVATE_KEY_ID: str = ""
    FIREBASE_PRIVATE_KEY: str = ""
    FIREBASE_CLIENT_EMAIL: str = ""
    FIREBASE_CLIENT_ID: str = ""
    FIREBASE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    FIREBASE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"
    FIREBASE_STORAGE_BUCKET: str = "agro-bot-automation.appspot.com"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    ALLOWED_DOCUMENT_EXTENSIONS: List[str] = [".pdf", ".doc", ".docx", ".txt"]
    UPLOAD_DIR: str = "uploads"
    
    # AI/ML Configuration
    AI_SERVICE_URL: str = "http://localhost:8001"
    AI_API_KEY: str = "agro-bot-ai-api-key"
    
    # Disease Detection Model
    DISEASE_MODEL_PATH: str = "models/disease_detection.h5"
    DISEASE_MODEL_VERSION: str = "1.0"
    DISEASE_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Pest Detection Model  
    PEST_MODEL_PATH: str = "models/pest_detection.h5"
    PEST_MODEL_VERSION: str = "1.0"
    PEST_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Weather API
    WEATHER_API_KEY: str = "your-weather-api-key"
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # SMS Configuration (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@agro-bot.com"
    
    # Payment Gateway (Stripe)
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "agro-bot-files"
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT: str = "agro-bot-automation"
    GOOGLE_APPLICATION_CREDENTIALS: str = "firebase-config.json"
    
    # IoT Configuration
    IOT_BROKER_HOST: str = "localhost"
    IOT_BROKER_PORT: int = 1883
    IOT_BROKER_USERNAME: str = "agro_iot"
    IOT_BROKER_PASSWORD: str = "iot_password"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/agro_bot.log"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Feature Flags
    ENABLE_AI_FEATURES: bool = True
    ENABLE_IOT_FEATURES: bool = True
    ENABLE_MARKETPLACE: bool = True
    ENABLE_CHAT_ASSISTANT: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    
    @validator('CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator('ALLOWED_HOSTS', pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Database configuration for different environments
def get_database_url() -> str:
    """Get database URL based on environment"""
    if settings.ENVIRONMENT == "test":
        return "postgresql://agro_user:agro_password@localhost:5432/agro_bot_test_db"
    elif settings.ENVIRONMENT == "production":
        return settings.DATABASE_URL
    else:
        return settings.DATABASE_URL


# Redis configuration for different environments  
def get_redis_url() -> str:
    """Get Redis URL based on environment"""
    if settings.ENVIRONMENT == "test":
        return "redis://localhost:6379/1"
    else:
        return settings.REDIS_URL


# Firebase configuration
def get_firebase_config() -> dict:
    """Get Firebase configuration"""
    return {
        "type": "service_account",
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
        "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": settings.FIREBASE_CLIENT_ID,
        "auth_uri": settings.FIREBASE_AUTH_URI,
        "token_uri": settings.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    }