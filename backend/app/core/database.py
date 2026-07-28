"""
Database configuration for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import logging

from app.core.config import settings, get_database_url

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    get_database_url(),
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    connect_args={
        "check_same_thread": False
    } if "sqlite" in get_database_url() else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    """
    try:
        # Import all models to ensure they are registered
        from app.models import (
            User, Farmer, Farm, Plot, CropVariety, Crop,
            Device, SensorReading, WeatherData, WeatherForecast,
            DiseaseDetection, PestDetection, IrrigationSchedule, IrrigationLog,
            FertilizerRecommendation, FertilizerApplication, YieldPrediction,
            MarketplaceCategory, MarketplaceProduct, MarketplaceOrder,
            GovernmentScheme, SchemeApplication, ChatConversation, ChatMessage,
            Notification, SystemAlert, AnalyticsEvent, AuditLog, ApiUsage
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_tables():
    """
    Drop all database tables (for development/testing)
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def test_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False