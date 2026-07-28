"""
Weather models for AGRO-BOT & AUTOMATION
"""

from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid

from app.core.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))
    pressure = Column(DECIMAL(7, 2))
    wind_speed = Column(DECIMAL(5, 2))
    wind_direction = Column(Integer)
    rainfall = Column(DECIMAL(6, 2))
    solar_radiation = Column(DECIMAL(8, 2))
    uv_index = Column(DECIMAL(3, 1))
    visibility = Column(DECIMAL(5, 2))
    weather_condition = Column(String(100))
    source = Column(String(50), default='api')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<WeatherData(temperature='{self.temperature}', timestamp='{self.timestamp}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'timestamp': self.timestamp.isoformat(),
            'temperature': float(self.temperature) if self.temperature else None,
            'humidity': float(self.humidity) if self.humidity else None,
            'pressure': float(self.pressure) if self.pressure else None,
            'wind_speed': float(self.wind_speed) if self.wind_speed else None,
            'wind_direction': self.wind_direction,
            'rainfall': float(self.rainfall) if self.rainfall else None,
            'solar_radiation': float(self.solar_radiation) if self.solar_radiation else None,
            'uv_index': float(self.uv_index) if self.uv_index else None,
            'visibility': float(self.visibility) if self.visibility else None,
            'weather_condition': self.weather_condition,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    forecast_date = Column(Date, nullable=False)
    min_temperature = Column(DECIMAL(5, 2))
    max_temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))
    wind_speed = Column(DECIMAL(5, 2))
    rainfall_probability = Column(DECIMAL(5, 2))
    expected_rainfall = Column(DECIMAL(6, 2))
    weather_condition = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<WeatherForecast(date='{self.forecast_date}', max_temp='{self.max_temperature}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'forecast_date': self.forecast_date.isoformat(),
            'min_temperature': float(self.min_temperature) if self.min_temperature else None,
            'max_temperature': float(self.max_temperature) if self.max_temperature else None,
            'humidity': float(self.humidity) if self.humidity else None,
            'wind_speed': float(self.wind_speed) if self.wind_speed else None,
            'rainfall_probability': float(self.rainfall_probability) if self.rainfall_probability else None,
            'expected_rainfall': float(self.expected_rainfall) if self.expected_rainfall else None,
            'weather_condition': self.weather_condition,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }