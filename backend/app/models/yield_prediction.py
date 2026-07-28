"""Yield Prediction models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class YieldPrediction(Base):
    __tablename__ = "yield_predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    prediction_date = Column(Date)
    predicted_yield = Column(DECIMAL(8, 2))
    confidence_interval_lower = Column(DECIMAL(8, 2))
    confidence_interval_upper = Column(DECIMAL(8, 2))
    prediction_accuracy = Column(DECIMAL(5, 4))
    factors_considered = Column(JSONB)
    ai_model_version = Column(String(50))
    market_price_prediction = Column(DECIMAL(8, 2))
    revenue_prediction = Column(DECIMAL(12, 2))
    harvest_window_start = Column(Date)
    harvest_window_end = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    crop = relationship("Crop", back_populates="yield_predictions")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'crop_id': str(self.crop_id), 'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'predicted_yield': float(self.predicted_yield) if self.predicted_yield else None,
            'confidence_interval_lower': float(self.confidence_interval_lower) if self.confidence_interval_lower else None,
            'confidence_interval_upper': float(self.confidence_interval_upper) if self.confidence_interval_upper else None,
            'prediction_accuracy': float(self.prediction_accuracy) if self.prediction_accuracy else None,
            'factors_considered': self.factors_considered, 'ai_model_version': self.ai_model_version,
            'market_price_prediction': float(self.market_price_prediction) if self.market_price_prediction else None,
            'revenue_prediction': float(self.revenue_prediction) if self.revenue_prediction else None,
            'harvest_window_start': self.harvest_window_start.isoformat() if self.harvest_window_start else None,
            'harvest_window_end': self.harvest_window_end.isoformat() if self.harvest_window_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }