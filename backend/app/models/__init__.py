"""
Database models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy.ext.declarative import declarative_base

# Create declarative base
Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .farmer import Farmer
from .farm import Farm, Plot
from .crop import CropVariety, Crop
from .device import Device, SensorReading
from .weather import WeatherData, WeatherForecast
from .disease import DiseaseDetection, PestDetection
from .irrigation import IrrigationSchedule, IrrigationLog
from .fertilizer import FertilizerRecommendation, FertilizerApplication
from .yield_prediction import YieldPrediction
from .marketplace import MarketplaceCategory, MarketplaceProduct, MarketplaceOrder
from .government import GovernmentScheme, SchemeApplication
from .chat import ChatConversation, ChatMessage
from .notification import Notification, SystemAlert
from .analytics import AnalyticsEvent, AuditLog, ApiUsage

__all__ = [
    "Base",
    "User",
    "Farmer", 
    "Farm",
    "Plot",
    "CropVariety",
    "Crop",
    "Device",
    "SensorReading",
    "WeatherData",
    "WeatherForecast", 
    "DiseaseDetection",
    "PestDetection",
    "IrrigationSchedule",
    "IrrigationLog",
    "FertilizerRecommendation",
    "FertilizerApplication",
    "YieldPrediction",
    "MarketplaceCategory",
    "MarketplaceProduct", 
    "MarketplaceOrder",
    "GovernmentScheme",
    "SchemeApplication",
    "ChatConversation",
    "ChatMessage",
    "Notification",
    "SystemAlert",
    "AnalyticsEvent",
    "AuditLog",
    "ApiUsage"
]