"""
Farmer model for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(String(50), unique=True, index=True)
    address = Column(Text)
    district = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    total_land_area = Column(DECIMAL(10, 2))
    experience_years = Column(Integer)
    education_level = Column(String(50))
    annual_income = Column(DECIMAL(12, 2))
    bank_account_number = Column(String(50))
    ifsc_code = Column(String(20))
    aadhaar_number = Column(String(12))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="farmer_profile")
    farms = relationship("Farm", back_populates="farmer", cascade="all, delete-orphan")
    marketplace_products = relationship("MarketplaceProduct", back_populates="seller")
    scheme_applications = relationship("SchemeApplication", back_populates="farmer")

    def __repr__(self):
        return f"<Farmer(id='{self.farmer_id}', user_id='{self.user_id}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'farmer_id': self.farmer_id,
            'address': self.address,
            'district': self.district,
            'state': self.state,
            'pincode': self.pincode,
            'total_land_area': float(self.total_land_area) if self.total_land_area else None,
            'experience_years': self.experience_years,
            'education_level': self.education_level,
            'annual_income': float(self.annual_income) if self.annual_income else None,
            'bank_account_number': self.bank_account_number,
            'ifsc_code': self.ifsc_code,
            'aadhaar_number': self.aadhaar_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }