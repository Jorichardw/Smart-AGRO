"""
Farm service for AGRO-BOT & AUTOMATION
"""

from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text
import logging

from app.models.farm import Farm, Plot
from app.models.farmer import Farmer
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class FarmService(BaseService[Farm, dict, dict]):
    """
    Farm service for managing farm operations
    """
    
    def __init__(self, db: Session):
        super().__init__(Farm, db)
    
    def get_by_farmer_id(self, farmer_id: UUID, skip: int = 0, limit: int = 100) -> List[Farm]:
        """
        Get farms by farmer ID
        
        Args:
            farmer_id: Farmer ID
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farm]: List of farms for farmer
        """
        try:
            return self.db.query(Farm).filter(
                Farm.farmer_id == farmer_id
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting farms by farmer ID {farmer_id}: {e}")
            return []
    
    def get_by_location(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10,
        skip: int = 0,
        limit: int = 100
    ) -> List[Farm]:
        """
        Get farms near a location
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_km: Search radius in kilometers
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farm]: List of nearby farms
        """
        try:
            # PostGIS query for nearby farms
            query = self.db.query(Farm).filter(
                text(f"""
                ST_DWithin(
                    location,
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                    {radius_km * 1000}
                )
                """)
            )
            
            return query.offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting farms by location: {e}")
            return []
    
    def get_by_farm_type(self, farm_type: str, skip: int = 0, limit: int = 100) -> List[Farm]:
        """
        Get farms by type
        
        Args:
            farm_type: Farm type (organic, conventional, etc.)
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farm]: List of farms of specified type
        """
        try:
            return self.db.query(Farm).filter(
                Farm.farm_type == farm_type
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting farms by type {farm_type}: {e}")
            return []
    
    def search_farms(
        self,
        search_term: str,
        farmer_id: Optional[UUID] = None,
        farm_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Farm]:
        """
        Search farms by name or address
        
        Args:
            search_term: Search term
            farmer_id: Optional farmer ID filter
            farm_type: Optional farm type filter
            limit: Maximum results to return
            
        Returns:
            List[Farm]: List of matching farms
        """
        try:
            query = self.db.query(Farm)
            
            # Search filter
            if search_term:
                query = query.filter(
                    or_(
                        Farm.name.ilike(f"%{search_term}%"),
                        Farm.address.ilike(f"%{search_term}%"),
                        Farm.registration_number.ilike(f"%{search_term}%")
                    )
                )
            
            # Additional filters
            if farmer_id:
                query = query.filter(Farm.farmer_id == farmer_id)
            if farm_type:
                query = query.filter(Farm.farm_type == farm_type)
            
            return query.limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error searching farms: {e}")
            return []
    
    def get_farm_with_plots(self, farm_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get farm with all its plots
        
        Args:
            farm_id: Farm ID
            
        Returns:
            Optional[Dict[str, Any]]: Farm data with plots
        """
        try:
            farm = self.get_by_id(farm_id)
            if not farm:
                return None
            
            plots = self.db.query(Plot).filter(Plot.farm_id == farm_id).all()
            
            return {
                "farm": farm.to_dict(),
                "plots": [plot.to_dict() for plot in plots]
            }
            
        except Exception as e:
            logger.error(f"Error getting farm with plots {farm_id}: {e}")
            return None
    
    def get_farm_stats(self, farm_id: Optional[UUID] = None) -> Dict[str, Any]:
        """
        Get farm statistics
        
        Args:
            farm_id: Optional specific farm ID
            
        Returns:
            Dict[str, Any]: Farm statistics
        """
        try:
            if farm_id:
                # Stats for specific farm
                farm = self.get_by_id(farm_id)
                if not farm:
                    return {}
                
                plot_count = self.db.query(Plot).filter(Plot.farm_id == farm_id).count()
                total_plot_area = self.db.query(func.sum(Plot.area)).filter(
                    Plot.farm_id == farm_id
                ).scalar() or 0
                
                return {
                    "farm_id": str(farm_id),
                    "total_area": float(farm.total_area) if farm.total_area else 0,
                    "plot_count": plot_count,
                    "total_plot_area": float(total_plot_area),
                    "farm_type": farm.farm_type.value if farm.farm_type else None,
                    "ownership_type": farm.ownership_type.value if farm.ownership_type else None
                }
            else:
                # Global farm stats
                total_farms = self.count()
                
                # Area stats
                area_stats = self.db.query(
                    func.avg(Farm.total_area),
                    func.min(Farm.total_area),
                    func.max(Farm.total_area),
                    func.sum(Farm.total_area)
                ).filter(Farm.total_area.isnot(None)).first()
                
                # Farm type distribution
                type_dist = self.db.query(
                    Farm.farm_type,
                    func.count(Farm.id)
                ).group_by(Farm.farm_type).all()
                
                # Ownership distribution
                ownership_dist = self.db.query(
                    Farm.ownership_type,
                    func.count(Farm.id)
                ).group_by(Farm.ownership_type).all()
                
                return {
                    "total_farms": total_farms,
                    "total_area": {
                        "average": float(area_stats[0]) if area_stats[0] else 0,
                        "minimum": float(area_stats[1]) if area_stats[1] else 0,
                        "maximum": float(area_stats[2]) if area_stats[2] else 0,
                        "total": float(area_stats[3]) if area_stats[3] else 0
                    },
                    "farm_type_distribution": {
                        str(farm_type): count for farm_type, count in type_dist if farm_type
                    },
                    "ownership_distribution": {
                        str(ownership): count for ownership, count in ownership_dist if ownership
                    }
                }
                
        except Exception as e:
            logger.error(f"Error getting farm stats: {e}")
            return {}


class PlotService(BaseService[Plot, dict, dict]):
    """
    Plot service for managing farm plot operations
    """
    
    def __init__(self, db: Session):
        super().__init__(Plot, db)
    
    def get_by_farm_id(self, farm_id: UUID, skip: int = 0, limit: int = 100) -> List[Plot]:
        """
        Get plots by farm ID
        
        Args:
            farm_id: Farm ID
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Plot]: List of plots for farm
        """
        try:
            return self.db.query(Plot).filter(
                Plot.farm_id == farm_id
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting plots by farm ID {farm_id}: {e}")
            return []
    
    def get_plots_needing_soil_test(self, days_since_test: int = 365) -> List[Plot]:
        """
        Get plots that need soil testing
        
        Args:
            days_since_test: Days since last soil test
            
        Returns:
            List[Plot]: List of plots needing soil test
        """
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now().date() - timedelta(days=days_since_test)
            
            return self.db.query(Plot).filter(
                or_(
                    Plot.last_soil_test.is_(None),
                    Plot.last_soil_test < cutoff_date
                )
            ).all()
            
        except Exception as e:
            logger.error(f"Error getting plots needing soil test: {e}")
            return []
    
    def get_plots_by_soil_health(
        self,
        min_ph: Optional[float] = None,
        max_ph: Optional[float] = None,
        min_nitrogen: Optional[float] = None,
        min_phosphorus: Optional[float] = None,
        min_potassium: Optional[float] = None
    ) -> List[Plot]:
        """
        Get plots by soil health parameters
        
        Args:
            min_ph: Minimum soil pH
            max_ph: Maximum soil pH
            min_nitrogen: Minimum nitrogen level
            min_phosphorus: Minimum phosphorus level
            min_potassium: Minimum potassium level
            
        Returns:
            List[Plot]: List of plots matching criteria
        """
        try:
            query = self.db.query(Plot)
            
            if min_ph is not None:
                query = query.filter(Plot.soil_ph >= min_ph)
            if max_ph is not None:
                query = query.filter(Plot.soil_ph <= max_ph)
            if min_nitrogen is not None:
                query = query.filter(Plot.nitrogen_level >= min_nitrogen)
            if min_phosphorus is not None:
                query = query.filter(Plot.phosphorus_level >= min_phosphorus)
            if min_potassium is not None:
                query = query.filter(Plot.potassium_level >= min_potassium)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Error getting plots by soil health: {e}")
            return []
    
    def get_plot_stats(self, farm_id: Optional[UUID] = None) -> Dict[str, Any]:
        """
        Get plot statistics
        
        Args:
            farm_id: Optional specific farm ID
            
        Returns:
            Dict[str, Any]: Plot statistics
        """
        try:
            query = self.db.query(Plot)
            if farm_id:
                query = query.filter(Plot.farm_id == farm_id)
            
            total_plots = query.count()
            
            # Area stats
            area_stats = query.filter(Plot.area.isnot(None)).with_entities(
                func.avg(Plot.area),
                func.min(Plot.area),
                func.max(Plot.area),
                func.sum(Plot.area)
            ).first()
            
            # Soil health stats
            ph_stats = query.filter(Plot.soil_ph.isnot(None)).with_entities(
                func.avg(Plot.soil_ph),
                func.min(Plot.soil_ph),
                func.max(Plot.soil_ph)
            ).first()
            
            npk_stats = query.filter(
                Plot.nitrogen_level.isnot(None),
                Plot.phosphorus_level.isnot(None),
                Plot.potassium_level.isnot(None)
            ).with_entities(
                func.avg(Plot.nitrogen_level),
                func.avg(Plot.phosphorus_level),
                func.avg(Plot.potassium_level)
            ).first()
            
            return {
                "total_plots": total_plots,
                "area": {
                    "average": float(area_stats[0]) if area_stats[0] else 0,
                    "minimum": float(area_stats[1]) if area_stats[1] else 0,
                    "maximum": float(area_stats[2]) if area_stats[2] else 0,
                    "total": float(area_stats[3]) if area_stats[3] else 0
                },
                "soil_ph": {
                    "average": float(ph_stats[0]) if ph_stats[0] else 0,
                    "minimum": float(ph_stats[1]) if ph_stats[1] else 0,
                    "maximum": float(ph_stats[2]) if ph_stats[2] else 0
                },
                "soil_nutrients": {
                    "nitrogen_avg": float(npk_stats[0]) if npk_stats[0] else 0,
                    "phosphorus_avg": float(npk_stats[1]) if npk_stats[1] else 0,
                    "potassium_avg": float(npk_stats[2]) if npk_stats[2] else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting plot stats: {e}")
            return {}