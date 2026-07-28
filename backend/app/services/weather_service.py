"""
Weather service for AGRO-BOT & AUTOMATION
"""

import httpx
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.weather import WeatherData, WeatherForecast
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class WeatherService(BaseService[WeatherData, dict, dict]):
    """Weather service for external API integration and local storage"""
    
    def __init__(self, db: Session):
        super().__init__(WeatherData, db)
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_URL
        
    async def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get current weather from external API
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            Dict[str, Any]: Current weather data
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # OpenWeatherMap API call
                url = f"{self.base_url}/weather"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Transform to our format
                weather_data = {
                    "temperature": data.get("main", {}).get("temp"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "wind_direction": data.get("wind", {}).get("deg"),
                    "weather_condition": data.get("weather", [{}])[0].get("description"),
                    "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                    "timestamp": datetime.utcnow(),
                    "source": "openweather"
                }
                
                # Store in database
                await self._store_weather_data(latitude, longitude, weather_data)
                
                return weather_data
                
        except httpx.TimeoutException:
            logger.error("Weather API timeout")
            return await self._get_cached_weather(latitude, longitude)
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return await self._get_cached_weather(latitude, longitude)
    
    async def get_weather_forecast(
        self, 
        latitude: float, 
        longitude: float, 
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get weather forecast from external API
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of forecast days
            
        Returns:
            List[Dict[str, Any]]: Weather forecast data
        """
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # OpenWeatherMap 5-day forecast
                url = f"{self.base_url}/forecast"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                forecast_list = data.get("list", [])
                
                # Group by day and get daily forecasts
                daily_forecasts = []
                processed_dates = set()
                
                for item in forecast_list[:days * 8]:  # 8 forecasts per day (3-hour intervals)
                    forecast_date = datetime.fromtimestamp(item["dt"]).date()
                    
                    if forecast_date not in processed_dates:
                        daily_forecast = {
                            "date": forecast_date,
                            "min_temperature": item["main"]["temp_min"],
                            "max_temperature": item["main"]["temp_max"],
                            "humidity": item["main"]["humidity"],
                            "wind_speed": item["wind"]["speed"],
                            "rainfall_probability": item.get("pop", 0) * 100,
                            "weather_condition": item["weather"][0]["description"],
                            "expected_rainfall": item.get("rain", {}).get("3h", 0)
                        }
                        
                        daily_forecasts.append(daily_forecast)
                        processed_dates.add(forecast_date)
                        
                        # Store in database
                        await self._store_forecast_data(latitude, longitude, daily_forecast)
                
                return daily_forecasts[:days]
                
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {e}")
            return await self._get_cached_forecast(latitude, longitude, days)
    
    async def _store_weather_data(self, latitude: float, longitude: float, weather_data: Dict[str, Any]):
        """Store weather data in database"""
        try:
            from sqlalchemy import text
            
            weather_record = {
                "location": text(f"ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)"),
                "timestamp": weather_data["timestamp"],
                "temperature": weather_data.get("temperature"),
                "humidity": weather_data.get("humidity"),
                "pressure": weather_data.get("pressure"),
                "wind_speed": weather_data.get("wind_speed"),
                "wind_direction": weather_data.get("wind_direction"),
                "weather_condition": weather_data.get("weather_condition"),
                "visibility": weather_data.get("visibility"),
                "source": weather_data.get("source", "api")
            }
            
            self.create(weather_record)
            logger.info(f"Stored weather data for location: {latitude}, {longitude}")
            
        except Exception as e:
            logger.error(f"Error storing weather data: {e}")
    
    async def _store_forecast_data(self, latitude: float, longitude: float, forecast_data: Dict[str, Any]):
        """Store forecast data in database"""
        try:
            from sqlalchemy import text
            from app.models.weather import WeatherForecast
            
            forecast_record = WeatherForecast(
                location=text(f"ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)"),
                forecast_date=forecast_data["date"],
                min_temperature=forecast_data.get("min_temperature"),
                max_temperature=forecast_data.get("max_temperature"),
                humidity=forecast_data.get("humidity"),
                wind_speed=forecast_data.get("wind_speed"),
                rainfall_probability=forecast_data.get("rainfall_probability"),
                expected_rainfall=forecast_data.get("expected_rainfall"),
                weather_condition=forecast_data.get("weather_condition")
            )
            
            self.db.add(forecast_record)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error storing forecast data: {e}")
    
    async def _get_cached_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get cached weather data from database"""
        try:
            from sqlalchemy import text, desc
            
            # Get most recent weather data within 50km
            weather_record = self.db.query(WeatherData).filter(
                text(f"""
                ST_DWithin(
                    location,
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                    50000
                )
                """)
            ).order_by(desc(WeatherData.timestamp)).first()
            
            if weather_record:
                return weather_record.to_dict()
            
            # Return default weather if no cached data
            return {
                "temperature": None,
                "humidity": None,
                "weather_condition": "Data unavailable",
                "message": "Weather service temporarily unavailable"
            }
            
        except Exception as e:
            logger.error(f"Error getting cached weather: {e}")
            return {"error": "Weather data unavailable"}
    
    async def _get_cached_forecast(self, latitude: float, longitude: float, days: int) -> List[Dict[str, Any]]:
        """Get cached forecast data from database"""
        try:
            from sqlalchemy import text
            from app.models.weather import WeatherForecast
            
            forecasts = self.db.query(WeatherForecast).filter(
                text(f"""
                ST_DWithin(
                    location,
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                    50000
                )
                """)
            ).order_by(WeatherForecast.forecast_date).limit(days).all()
            
            return [forecast.to_dict() for forecast in forecasts]
            
        except Exception as e:
            logger.error(f"Error getting cached forecast: {e}")
            return []
    
    async def get_weather_alerts(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """
        Get weather alerts for location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            List[Dict[str, Any]]: Weather alerts
        """
        try:
            weather_data = await self.get_current_weather(latitude, longitude)
            alerts = []
            
            # Generate alerts based on weather conditions
            if weather_data.get("temperature", 0) > 40:
                alerts.append({
                    "type": "heat_wave",
                    "severity": "high",
                    "message": "Extreme heat warning. Consider adjusting irrigation schedule.",
                    "recommendations": [
                        "Increase irrigation frequency",
                        "Provide shade for crops",
                        "Avoid field work during peak hours"
                    ]
                })
            
            if weather_data.get("wind_speed", 0) > 15:
                alerts.append({
                    "type": "high_wind",
                    "severity": "medium",
                    "message": "High wind speeds detected. Secure equipment and structures.",
                    "recommendations": [
                        "Secure loose equipment",
                        "Check greenhouse structures",
                        "Delay spraying operations"
                    ]
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error generating weather alerts: {e}")
            return []
    
    def get_weather_history(
        self, 
        latitude: float, 
        longitude: float, 
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get historical weather data
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days_back: Number of days to look back
            
        Returns:
            List[Dict[str, Any]]: Historical weather data
        """
        try:
            from sqlalchemy import text, desc
            from datetime import timedelta
            
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            
            weather_records = self.db.query(WeatherData).filter(
                text(f"""
                ST_DWithin(
                    location,
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                    25000
                ) AND timestamp >= '{cutoff_date.isoformat()}'
                """)
            ).order_by(desc(WeatherData.timestamp)).all()
            
            return [record.to_dict() for record in weather_records]
            
        except Exception as e:
            logger.error(f"Error getting weather history: {e}")
            return []