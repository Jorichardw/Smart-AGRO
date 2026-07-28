"""
Farmer service for AGRO-BOT & AUTOMATION
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
import logging

from app.models.farmer import Farmer
from app.models.user import User
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class FarmerService(BaseService[Farmer, dict, dict]):
    """
    Farmer service for managing farmer operations
    """
    
    def __init__(self, db: Session):
        super().__init__(Farmer, db)
    
    def get_by_user_id(self, user_id: UUID) -> Optional[Farmer]:
        """
        Get farmer by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[Farmer]: Farmer instance or None
        """
        try:
            return self.db.query(Farmer).filter(Farmer.user_id == user_id).first()
        except Exception as e:
            logger.error(f"Error getting farmer by user ID {user_id}: {e}")
            return None
    
    def get_by_farmer_id(self, farmer_id: str) -> Optional[Farmer]:
        """
        Get farmer by government farmer ID
        
        Args:
            farmer_id: Government farmer ID
            
        Returns:
            Optional[Farmer]: Farmer instance or None
        """
        try:
            return self.db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
        except Exception as e:
            logger.error(f"Error getting farmer by farmer ID {farmer_id}: {e}")
            return None
    
    def get_by_district(self, district: str, skip: int = 0, limit: int = 100) -> List[Farmer]:
        """
        Get farmers by district
        
        Args:
            district: District name
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farmer]: List of farmers in district
        """
        try:
            return self.db.query(Farmer).filter(
                Farmer.district.ilike(f"%{district}%")
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting farmers by district {district}: {e}")
            return []
    
    def get_by_state(self, state: str, skip: int = 0, limit: int = 100) -> List[Farmer]:
        """
        Get farmers by state
        
        Args:
            state: State name
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farmer]: List of farmers in state
        """
        try:
            return self.db.query(Farmer).filter(
                Farmer.state.ilike(f"%{state}%")
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting farmers by state {state}: {e}")
            return []
    
    def search_farmers(
        self, 
        search_term: str, 
        district: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search farmers with optional location filters
        
        Args:
            search_term: Search term
            district: District filter
            state: State filter
            limit: Maximum results to return
            
        Returns:
            List[Dict[str, Any]]: List of farmer data with user info
        """
        try:
            query = self.db.query(Farmer, User).join(User, Farmer.user_id == User.id)
            
            # Apply search filter
            if search_term:
                query = query.filter(
                    or_(
                        Farmer.farmer_id.ilike(f"%{search_term}%"),
                        User.first_name.ilike(f"%{search_term}%"),
                        User.last_name.ilike(f"%{search_term}%"),
                        User.email.ilike(f"%{search_term}%"),
                        Farmer.address.ilike(f"%{search_term}%")
                    )
                )
            
            # Apply location filters
            if district:
                query = query.filter(Farmer.district.ilike(f"%{district}%"))
            if state:
                query = query.filter(Farmer.state.ilike(f"%{state}%"))
            
            results = query.limit(limit).all()
            
            # Format results
            farmers_data = []
            for farmer, user in results:
                farmers_data.append({
                    "farmer": farmer.to_dict(),
                    "user": user.to_dict()
                })
            
            return farmers_data
            
        except Exception as e:
            logger.error(f"Error searching farmers with term {search_term}: {e}")
            return []
    
    def get_farmer_with_user(self, farmer_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get farmer with user information
        
        Args:
            farmer_id: Farmer ID
            
        Returns:
            Optional[Dict[str, Any]]: Farmer and user data
        """
        try:
            result = self.db.query(Farmer, User).join(
                User, Farmer.user_id == User.id
            ).filter(Farmer.id == farmer_id).first()
            
            if result:
                farmer, user = result
                return {
                    "farmer": farmer.to_dict(),
                    "user": user.to_dict()
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting farmer with user {farmer_id}: {e}")
            return None
    
    def get_farmers_by_land_area(
        self, 
        min_area: Optional[float] = None,
        max_area: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Farmer]:
        """
        Get farmers by land area range
        
        Args:
            min_area: Minimum land area in acres
            max_area: Maximum land area in acres
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farmer]: List of farmers in area range
        """
        try:
            query = self.db.query(Farmer)
            
            if min_area is not None:
                query = query.filter(Farmer.total_land_area >= min_area)
            if max_area is not None:
                query = query.filter(Farmer.total_land_area <= max_area)
            
            return query.offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting farmers by land area: {e}")
            return []
    
    def get_farmers_by_experience(
        self, 
        min_years: Optional[int] = None,
        max_years: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Farmer]:
        """
        Get farmers by experience range
        
        Args:
            min_years: Minimum experience years
            max_years: Maximum experience years
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[Farmer]: List of farmers in experience range
        """
        try:
            query = self.db.query(Farmer)
            
            if min_years is not None:
                query = query.filter(Farmer.experience_years >= min_years)
            if max_years is not None:
                query = query.filter(Farmer.experience_years <= max_years)
            
            return query.offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting farmers by experience: {e}")
            return []
    
    def get_farmer_stats(self) -> Dict[str, Any]:
        """
        Get farmer statistics
        
        Returns:
            Dict[str, Any]: Farmer statistics
        """
        try:
            total_farmers = self.count()
            
            # Land area stats
            land_stats = self.db.query(
                func.avg(Farmer.total_land_area),
                func.min(Farmer.total_land_area),
                func.max(Farmer.total_land_area),
                func.sum(Farmer.total_land_area)
            ).filter(Farmer.total_land_area.isnot(None)).first()
            
            # Experience stats
            experience_stats = self.db.query(
                func.avg(Farmer.experience_years),
                func.min(Farmer.experience_years),
                func.max(Farmer.experience_years)
            ).filter(Farmer.experience_years.isnot(None)).first()
            
            # Education level distribution
            education_dist = self.db.query(
                Farmer.education_level,
                func.count(Farmer.id)
            ).group_by(Farmer.education_level).all()
            
            # State distribution
            state_dist = self.db.query(
                Farmer.state,
                func.count(Farmer.id)
            ).group_by(Farmer.state).order_by(func.count(Farmer.id).desc()).limit(10).all()
            
            return {
                "total_farmers": total_farmers,
                "land_area": {
                    "average": float(land_stats[0]) if land_stats[0] else 0,
                    "minimum": float(land_stats[1]) if land_stats[1] else 0,
                    "maximum": float(land_stats[2]) if land_stats[2] else 0,
                    "total": float(land_stats[3]) if land_stats[3] else 0
                },
                "experience": {
                    "average": float(experience_stats[0]) if experience_stats[0] else 0,
                    "minimum": int(experience_stats[1]) if experience_stats[1] else 0,
                    "maximum": int(experience_stats[2]) if experience_stats[2] else 0
                },
                "education_distribution": {level: count for level, count in education_dist if level},
                "top_states": {state: count for state, count in state_dist if state}
            }
            
        except Exception as e:
            logger.error(f"Error getting farmer stats: {e}")
            return {}
    
    def check_farmer_id_exists(self, farmer_id: str, exclude_farmer_id: Optional[UUID] = None) -> bool:
        """
        Check if government farmer ID already exists
        
        Args:
            farmer_id: Government farmer ID to check
            exclude_farmer_id: Farmer ID to exclude from check
            
        Returns:
            bool: True if farmer ID exists
        """
        try:
            query = self.db.query(Farmer).filter(Farmer.farmer_id == farmer_id)
            if exclude_farmer_id:
                query = query.filter(Farmer.id != exclude_farmer_id)
            return query.first() is not None
        except Exception as e:
            logger.error(f"Error checking farmer ID existence {farmer_id}: {e}")
            return False