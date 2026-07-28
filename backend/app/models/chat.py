"""Chat models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base

class MessageType(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatConversation(Base):
    __tablename__ = "chat_conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_title = Column(String(300))
    language = Column(String(10), default='en')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'user_id': str(self.user_id), 'conversation_title': self.conversation_title,
            'language': self.language, 'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("chat_conversations.id", ondelete="CASCADE"), nullable=False)
    message_type = Column(Enum(MessageType))
    message_text = Column(Text, nullable=False)
    message_audio_url = Column(Text)
    attachments = Column(JSONB)
    context_data = Column(JSONB)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("ChatConversation", back_populates="messages")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'conversation_id': str(self.conversation_id), 'message_type': self.message_type.value if self.message_type else None,
            'message_text': self.message_text, 'message_audio_url': self.message_audio_url,
            'attachments': self.attachments, 'context_data': self.context_data,
            'timestamp': self.timestamp.isoformat()
        }