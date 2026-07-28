"""Notification models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
import enum
from app.core.database import Base

class NotificationType(str, enum.Enum):
    WEATHER_ALERT = "weather_alert"
    IRRIGATION_REMINDER = "irrigation_reminder"
    DISEASE_DETECTED = "disease_detected"
    PEST_DETECTED = "pest_detected"
    HARVEST_REMINDER = "harvest_reminder"
    FERTILIZER_REMINDER = "fertilizer_reminder"
    SCHEME_UPDATE = "scheme_update"
    MARKET_PRICE = "market_price"
    ORDER_UPDATE = "order_update"
    SYSTEM = "system"

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType))
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    data = Column(JSONB)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    action_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'user_id': str(self.user_id), 'title': self.title, 'message': self.message,
            'notification_type': self.notification_type.value if self.notification_type else None,
            'priority': self.priority.value if self.priority else None, 'data': self.data,
            'is_read': self.is_read, 'read_at': self.read_at.isoformat() if self.read_at else None,
            'sent_at': self.sent_at.isoformat(), 'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'action_url': self.action_url, 'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SystemAlert(Base):
    __tablename__ = "system_alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type = Column(String(100), nullable=False)
    severity = Column(Enum(AlertSeverity))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    affected_area = Column(Geography(geometry_type='POLYGON', srid=4326))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    source = Column(String(100))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            'id': str(self.id), 'alert_type': self.alert_type, 'severity': self.severity.value if self.severity else None,
            'title': self.title, 'description': self.description,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_active': self.is_active, 'source': self.source, 'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }