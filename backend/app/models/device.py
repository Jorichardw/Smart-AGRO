"""
IoT Device models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, Enum, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
import enum

from app.core.database import Base


class DeviceType(str, enum.Enum):
    SENSOR_NODE = "sensor_node"
    WEATHER_STATION = "weather_station"
    IRRIGATION_CONTROLLER = "irrigation_controller"
    CAMERA = "camera"
    GATEWAY = "gateway"


class DeviceStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200))
    device_type = Column(Enum(DeviceType))
    model = Column(String(100))
    manufacturer = Column(String(100))
    location = Column(Geography(geometry_type='POINT', srid=4326))
    installation_date = Column(Date)
    last_maintenance = Column(Date)
    battery_level = Column(Integer)
    signal_strength = Column(Integer)
    firmware_version = Column(String(50))
    configuration = Column(JSONB)
    is_active = Column(Boolean, default=True)
    status = Column(Enum(DeviceStatus), default=DeviceStatus.ONLINE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    farm = relationship("Farm", back_populates="devices")
    sensor_readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan")
    irrigation_logs = relationship("IrrigationLog", back_populates="device")

    def __repr__(self):
        return f"<Device(device_id='{self.device_id}', type='{self.device_type}', status='{self.status}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'farm_id': str(self.farm_id),
            'device_id': self.device_id,
            'name': self.name,
            'device_type': self.device_type.value if self.device_type else None,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'last_maintenance': self.last_maintenance.isoformat() if self.last_maintenance else None,
            'battery_level': self.battery_level,
            'signal_strength': self.signal_strength,
            'firmware_version': self.firmware_version,
            'configuration': self.configuration,
            'is_active': self.is_active,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    sensor_type = Column(String(100), nullable=False)
    value = Column(DECIMAL(10, 4), nullable=False)
    unit = Column(String(20))
    quality_score = Column(Integer)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    device = relationship("Device", back_populates="sensor_readings")

    def __repr__(self):
        return f"<SensorReading(device_id='{self.device_id}', type='{self.sensor_type}', value='{self.value}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'device_id': str(self.device_id),
            'sensor_type': self.sensor_type,
            'value': float(self.value),
            'unit': self.unit,
            'quality_score': self.quality_score,
            'timestamp': self.timestamp.isoformat(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }