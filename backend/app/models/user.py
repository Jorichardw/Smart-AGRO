"""
User model for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    AGRICULTURE_OFFICER = "agriculture_officer"
    EXPERT = "expert"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.FARMER, nullable=False)
    profile_image_url = Column(String(500))
    language_preference = Column(String(10), default='en')
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    farmer_profile = relationship("Farmer", back_populates="user", uselist=False)
    disease_detections = relationship("DiseaseDetection", back_populates="user")
    pest_detections = relationship("PestDetection", back_populates="user")
    chat_conversations = relationship("ChatConversation", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    analytics_events = relationship("AnalyticsEvent", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email

    def to_dict(self):
        return {
            'id': str(self.id),
            'firebase_uid': self.firebase_uid,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role.value if self.role else None,
            'profile_image_url': self.profile_image_url,
            'language_preference': self.language_preference,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }