"""
Farm and Plot models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Text, DECIMAL, ForeignKey, DateTime, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
import enum

from app.core.database import Base


class FarmType(str, enum.Enum):
    ORGANIC = "organic"
    CONVENTIONAL = "conventional" 
    HYDROPONIC = "hydroponic"
    GREENHOUSE = "greenhouse"


class OwnershipType(str, enum.Enum):
    OWNED = "owned"
    LEASED = "leased"
    SHARECROP = "sharecrop"


class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    address = Column(Text)
    total_area = Column(DECIMAL(10, 2))
    soil_type = Column(String(100))
    irrigation_type = Column(String(100))
    elevation = Column(DECIMAL(8, 2))
    farm_type = Column(Enum(FarmType))
    ownership_type = Column(Enum(OwnershipType))
    registration_number = Column(String(100))
    images = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    farmer = relationship("Farmer", back_populates="farms")
    plots = relationship("Plot", back_populates="farm", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="farm", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Farm(name='{self.name}', farmer_id='{self.farmer_id}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'farmer_id': str(self.farmer_id),
            'name': self.name,
            'address': self.address,
            'total_area': float(self.total_area) if self.total_area else None,
            'soil_type': self.soil_type,
            'irrigation_type': self.irrigation_type,
            'elevation': float(self.elevation) if self.elevation else None,
            'farm_type': self.farm_type.value if self.farm_type else None,
            'ownership_type': self.ownership_type.value if self.ownership_type else None,
            'registration_number': self.registration_number,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Plot(Base):
    __tablename__ = "plots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    area = Column(DECIMAL(8, 2))
    soil_ph = Column(DECIMAL(3, 1))
    soil_ec = Column(DECIMAL(5, 2))
    organic_matter = Column(DECIMAL(5, 2))
    nitrogen_level = Column(DECIMAL(5, 2))
    phosphorus_level = Column(DECIMAL(5, 2))
    potassium_level = Column(DECIMAL(5, 2))
    last_soil_test = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    farm = relationship("Farm", back_populates="plots")
    crops = relationship("Crop", back_populates="plot", cascade="all, delete-orphan")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="plot")
    irrigation_logs = relationship("IrrigationLog", back_populates="plot")

    def __repr__(self):
        return f"<Plot(name='{self.name}', farm_id='{self.farm_id}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'farm_id': str(self.farm_id),
            'name': self.name,
            'area': float(self.area) if self.area else None,
            'soil_ph': float(self.soil_ph) if self.soil_ph else None,
            'soil_ec': float(self.soil_ec) if self.soil_ec else None,
            'organic_matter': float(self.organic_matter) if self.organic_matter else None,
            'nitrogen_level': float(self.nitrogen_level) if self.nitrogen_level else None,
            'phosphorus_level': float(self.phosphorus_level) if self.phosphorus_level else None,
            'potassium_level': float(self.potassium_level) if self.potassium_level else None,
            'last_soil_test': self.last_soil_test.isoformat() if self.last_soil_test else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }