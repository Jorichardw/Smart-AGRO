"""
Crop models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class Season(str, enum.Enum):
    KHARIF = "kharif"
    RABI = "rabi"
    SUMMER = "summer"
    YEAR_ROUND = "year_round"


class CropStatus(str, enum.Enum):
    PLANNING = "planning"
    PLANTED = "planted"
    GROWING = "growing"
    FLOWERING = "flowering"
    HARVESTED = "harvested"
    FAILED = "failed"


class CropVariety(Base):
    __tablename__ = "crop_varieties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    scientific_name = Column(String(200))
    category = Column(String(100))
    variety = Column(String(200))
    season = Column(Enum(Season))
    growth_duration_days = Column(Integer)
    water_requirement = Column(String(50))
    soil_type_preference = Column(Text)
    temperature_range = Column(String(50))
    spacing_cm = Column(Integer)
    seed_rate_per_acre = Column(DECIMAL(8, 2))
    expected_yield_per_acre = Column(DECIMAL(8, 2))
    market_price_per_kg = Column(DECIMAL(8, 2))
    image_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    crops = relationship("Crop", back_populates="variety")

    def __repr__(self):
        return f"<CropVariety(name='{self.name}', category='{self.category}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'variety': self.variety,
            'season': self.season.value if self.season else None,
            'growth_duration_days': self.growth_duration_days,
            'water_requirement': self.water_requirement,
            'soil_type_preference': self.soil_type_preference,
            'temperature_range': self.temperature_range,
            'spacing_cm': self.spacing_cm,
            'seed_rate_per_acre': float(self.seed_rate_per_acre) if self.seed_rate_per_acre else None,
            'expected_yield_per_acre': float(self.expected_yield_per_acre) if self.expected_yield_per_acre else None,
            'market_price_per_kg': float(self.market_price_per_kg) if self.market_price_per_kg else None,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Crop(Base):
    __tablename__ = "crops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plot_id = Column(UUID(as_uuid=True), ForeignKey("plots.id", ondelete="CASCADE"), nullable=False)
    crop_variety_id = Column(UUID(as_uuid=True), ForeignKey("crop_varieties.id"), nullable=False)
    planting_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date)
    actual_harvest_date = Column(Date)
    area_planted = Column(DECIMAL(8, 2))
    seed_quantity = Column(DECIMAL(8, 2))
    seed_cost = Column(DECIMAL(10, 2))
    status = Column(Enum(CropStatus), default=CropStatus.GROWING)
    growth_stage = Column(String(100))
    expected_yield = Column(DECIMAL(8, 2))
    actual_yield = Column(DECIMAL(8, 2))
    notes = Column(Text)
    images = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    plot = relationship("Plot", back_populates="crops")
    variety = relationship("CropVariety", back_populates="crops")
    disease_detections = relationship("DiseaseDetection", back_populates="crop")
    pest_detections = relationship("PestDetection", back_populates="crop")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="crop")
    fertilizer_recommendations = relationship("FertilizerRecommendation", back_populates="crop")
    fertilizer_applications = relationship("FertilizerApplication", back_populates="crop")
    yield_predictions = relationship("YieldPrediction", back_populates="crop")

    def __repr__(self):
        return f"<Crop(variety_id='{self.crop_variety_id}', plot_id='{self.plot_id}', status='{self.status}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'plot_id': str(self.plot_id),
            'crop_variety_id': str(self.crop_variety_id),
            'planting_date': self.planting_date.isoformat() if self.planting_date else None,
            'expected_harvest_date': self.expected_harvest_date.isoformat() if self.expected_harvest_date else None,
            'actual_harvest_date': self.actual_harvest_date.isoformat() if self.actual_harvest_date else None,
            'area_planted': float(self.area_planted) if self.area_planted else None,
            'seed_quantity': float(self.seed_quantity) if self.seed_quantity else None,
            'seed_cost': float(self.seed_cost) if self.seed_cost else None,
            'status': self.status.value if self.status else None,
            'growth_stage': self.growth_stage,
            'expected_yield': float(self.expected_yield) if self.expected_yield else None,
            'actual_yield': float(self.actual_yield) if self.actual_yield else None,
            'notes': self.notes,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }