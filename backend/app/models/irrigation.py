"""
Irrigation models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime, Enum, Boolean, Date, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class IrrigationStatus(str, enum.Enum):
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"


class IrrigationSchedule(Base):
    __tablename__ = "irrigation_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plot_id = Column(UUID(as_uuid=True), ForeignKey("plots.id", ondelete="CASCADE"), nullable=False)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id"))
    schedule_name = Column(String(200))
    irrigation_method = Column(String(100))
    frequency_days = Column(Integer)
    duration_minutes = Column(Integer)
    water_amount_liters = Column(DECIMAL(10, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    time_of_day = Column(Time)
    is_active = Column(Boolean, default=True)
    auto_adjustment = Column(Boolean, default=True)
    weather_dependent = Column(Boolean, default=True)
    soil_moisture_threshold = Column(DECIMAL(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    plot = relationship("Plot", back_populates="irrigation_schedules")
    crop = relationship("Crop", back_populates="irrigation_schedules")
    irrigation_logs = relationship("IrrigationLog", back_populates="schedule")

    def __repr__(self):
        return f"<IrrigationSchedule(name='{self.schedule_name}', plot_id='{self.plot_id}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'plot_id': str(self.plot_id),
            'crop_id': str(self.crop_id) if self.crop_id else None,
            'schedule_name': self.schedule_name,
            'irrigation_method': self.irrigation_method,
            'frequency_days': self.frequency_days,
            'duration_minutes': self.duration_minutes,
            'water_amount_liters': float(self.water_amount_liters) if self.water_amount_liters else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'time_of_day': self.time_of_day.isoformat() if self.time_of_day else None,
            'is_active': self.is_active,
            'auto_adjustment': self.auto_adjustment,
            'weather_dependent': self.weather_dependent,
            'soil_moisture_threshold': float(self.soil_moisture_threshold) if self.soil_moisture_threshold else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class IrrigationLog(Base):
    __tablename__ = "irrigation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("irrigation_schedules.id"))
    plot_id = Column(UUID(as_uuid=True), ForeignKey("plots.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    planned_duration_minutes = Column(Integer)
    actual_duration_minutes = Column(Integer)
    water_used_liters = Column(DECIMAL(10, 2))
    trigger_reason = Column(String(100))
    soil_moisture_before = Column(DECIMAL(5, 2))
    soil_moisture_after = Column(DECIMAL(5, 2))
    status = Column(Enum(IrrigationStatus))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    schedule = relationship("IrrigationSchedule", back_populates="irrigation_logs")
    plot = relationship("Plot", back_populates="irrigation_logs")
    device = relationship("Device", back_populates="irrigation_logs")

    def __repr__(self):
        return f"<IrrigationLog(plot_id='{self.plot_id}', status='{self.status}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'schedule_id': str(self.schedule_id) if self.schedule_id else None,
            'plot_id': str(self.plot_id),
            'device_id': str(self.device_id) if self.device_id else None,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'planned_duration_minutes': self.planned_duration_minutes,
            'actual_duration_minutes': self.actual_duration_minutes,
            'water_used_liters': float(self.water_used_liters) if self.water_used_liters else None,
            'trigger_reason': self.trigger_reason,
            'soil_moisture_before': float(self.soil_moisture_before) if self.soil_moisture_before else None,
            'soil_moisture_after': float(self.soil_moisture_after) if self.soil_moisture_after else None,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }