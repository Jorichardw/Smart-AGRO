"""Fertilizer models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime, Enum, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base

class RecommendationStatus(str, enum.Enum):
    PENDING = "pending"
    APPLIED = "applied"
    CANCELLED = "cancelled"

class FertilizerRecommendation(Base):
    __tablename__ = "fertilizer_recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    recommended_by = Column(String(50), default='ai')
    fertilizer_type = Column(String(100))
    npk_ratio = Column(String(20))
    quantity_per_acre = Column(DECIMAL(8, 2))
    application_method = Column(String(100))
    application_timing = Column(String(200))
    frequency = Column(Integer)
    cost_per_kg = Column(DECIMAL(8, 2))
    total_cost = Column(DECIMAL(10, 2))
    benefits = Column(Text)
    application_instructions = Column(Text)
    precautions = Column(Text)
    is_organic = Column(Boolean, default=False)
    recommendation_date = Column(Date)
    valid_until = Column(Date)
    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    crop = relationship("Crop", back_populates="fertilizer_recommendations")
    applications = relationship("FertilizerApplication", back_populates="recommendation")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'crop_id': str(self.crop_id), 'recommended_by': self.recommended_by,
            'fertilizer_type': self.fertilizer_type, 'npk_ratio': self.npk_ratio,
            'quantity_per_acre': float(self.quantity_per_acre) if self.quantity_per_acre else None,
            'application_method': self.application_method, 'application_timing': self.application_timing,
            'frequency': self.frequency, 'cost_per_kg': float(self.cost_per_kg) if self.cost_per_kg else None,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'benefits': self.benefits, 'application_instructions': self.application_instructions,
            'precautions': self.precautions, 'is_organic': self.is_organic,
            'recommendation_date': self.recommendation_date.isoformat() if self.recommendation_date else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FertilizerApplication(Base):
    __tablename__ = "fertilizer_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey("fertilizer_recommendations.id"))
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    applied_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    fertilizer_name = Column(String(200))
    quantity_applied = Column(DECIMAL(8, 2))
    application_method = Column(String(100))
    application_date = Column(Date)
    weather_conditions = Column(Text)
    soil_conditions = Column(Text)
    cost = Column(DECIMAL(10, 2))
    notes = Column(Text)
    images = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    recommendation = relationship("FertilizerRecommendation", back_populates="applications")
    crop = relationship("Crop", back_populates="fertilizer_applications")
    applied_by_user = relationship("User")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'recommendation_id': str(self.recommendation_id) if self.recommendation_id else None,
            'crop_id': str(self.crop_id), 'applied_by': str(self.applied_by) if self.applied_by else None,
            'fertilizer_name': self.fertilizer_name, 'quantity_applied': float(self.quantity_applied) if self.quantity_applied else None,
            'application_method': self.application_method, 'application_date': self.application_date.isoformat() if self.application_date else None,
            'weather_conditions': self.weather_conditions, 'soil_conditions': self.soil_conditions,
            'cost': float(self.cost) if self.cost else None, 'notes': self.notes, 'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }