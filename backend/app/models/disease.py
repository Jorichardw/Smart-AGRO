"""
Disease and Pest Detection models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class Severity(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class PestSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = Column(Text, nullable=False)
    detected_disease = Column(String(200))
    confidence_score = Column(DECIMAL(5, 4))
    severity = Column(Enum(Severity))
    affected_area_percentage = Column(DECIMAL(5, 2))
    symptoms = Column(Text)
    causes = Column(Text)
    treatment_recommendations = Column(Text)
    organic_treatments = Column(Text)
    chemical_treatments = Column(Text)
    prevention_tips = Column(Text)
    detection_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ai_model_version = Column(String(50))
    is_verified = Column(Boolean, default=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    crop = relationship("Crop", back_populates="disease_detections")
    user = relationship("User", foreign_keys=[user_id], back_populates="disease_detections")
    verified_by_user = relationship("User", foreign_keys=[verified_by])

    def __repr__(self):
        return f"<DiseaseDetection(disease='{self.detected_disease}', confidence='{self.confidence_score}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'crop_id': str(self.crop_id),
            'user_id': str(self.user_id),
            'image_url': self.image_url,
            'detected_disease': self.detected_disease,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'severity': self.severity.value if self.severity else None,
            'affected_area_percentage': float(self.affected_area_percentage) if self.affected_area_percentage else None,
            'symptoms': self.symptoms,
            'causes': self.causes,
            'treatment_recommendations': self.treatment_recommendations,
            'organic_treatments': self.organic_treatments,
            'chemical_treatments': self.chemical_treatments,
            'prevention_tips': self.prevention_tips,
            'detection_timestamp': self.detection_timestamp.isoformat(),
            'ai_model_version': self.ai_model_version,
            'is_verified': self.is_verified,
            'verified_by': str(self.verified_by) if self.verified_by else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PestDetection(Base):
    __tablename__ = "pest_detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = Column(Text, nullable=False)
    detected_pest = Column(String(200))
    confidence_score = Column(DECIMAL(5, 4))
    severity = Column(Enum(PestSeverity))
    pest_count = Column(Integer)
    life_stage = Column(String(50))
    damage_description = Column(Text)
    treatment_recommendations = Column(Text)
    organic_treatments = Column(Text)
    chemical_treatments = Column(Text)
    prevention_measures = Column(Text)
    detection_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ai_model_version = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    crop = relationship("Crop", back_populates="pest_detections")
    user = relationship("User", back_populates="pest_detections")

    def __repr__(self):
        return f"<PestDetection(pest='{self.detected_pest}', confidence='{self.confidence_score}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'crop_id': str(self.crop_id),
            'user_id': str(self.user_id),
            'image_url': self.image_url,
            'detected_pest': self.detected_pest,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'severity': self.severity.value if self.severity else None,
            'pest_count': self.pest_count,
            'life_stage': self.life_stage,
            'damage_description': self.damage_description,
            'treatment_recommendations': self.treatment_recommendations,
            'organic_treatments': self.organic_treatments,
            'chemical_treatments': self.chemical_treatments,
            'prevention_measures': self.prevention_measures,
            'detection_timestamp': self.detection_timestamp.isoformat(),
            'ai_model_version': self.ai_model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }