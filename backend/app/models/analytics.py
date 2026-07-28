"""Analytics models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_type = Column(String(100), nullable=False)
    event_data = Column(JSONB)
    session_id = Column(String(100))
    ip_address = Column(INET)
    user_agent = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analytics_events")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'user_id': str(self.user_id) if self.user_id else None,
            'event_type': self.event_type, 'event_data': self.event_data,
            'session_id': self.session_id, 'ip_address': str(self.ip_address) if self.ip_address else None,
            'user_agent': self.user_agent, 'timestamp': self.timestamp.isoformat()
        }

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    table_name = Column(String(100))
    record_id = Column(UUID(as_uuid=True))
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'user_id': str(self.user_id) if self.user_id else None,
            'action': self.action, 'table_name': self.table_name, 'record_id': str(self.record_id) if self.record_id else None,
            'old_values': self.old_values, 'new_values': self.new_values,
            'ip_address': str(self.ip_address) if self.ip_address else None,
            'user_agent': self.user_agent, 'timestamp': self.timestamp.isoformat()
        }

class ApiUsage(Base):
    __tablename__ = "api_usage"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    endpoint = Column(String(200))
    method = Column(String(10))
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    request_size_bytes = Column(Integer)
    response_size_bytes = Column(Integer)
    ip_address = Column(INET)
    user_agent = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            'id': str(self.id), 'user_id': str(self.user_id) if self.user_id else None,
            'endpoint': self.endpoint, 'method': self.method, 'status_code': self.status_code,
            'response_time_ms': self.response_time_ms, 'request_size_bytes': self.request_size_bytes,
            'response_size_bytes': self.response_size_bytes, 'ip_address': str(self.ip_address) if self.ip_address else None,
            'user_agent': self.user_agent, 'timestamp': self.timestamp.isoformat()
        }