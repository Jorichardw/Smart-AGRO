"""
User service for AGRO-BOT & AUTOMATION
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_
import logging

from app.models.user import User
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class UserService(BaseService[User, dict, dict]):
    """
    User service for managing user operations
    """
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User instance or None
        """
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def get_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """
        Get user by Firebase UID
        
        Args:
            firebase_uid: Firebase user ID
            
        Returns:
            Optional[User]: User instance or None
        """
        try:
            return self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        except Exception as e:
            logger.error(f"Error getting user by Firebase UID {firebase_uid}: {e}")
            return None
    
    def get_by_phone(self, phone: str) -> Optional[User]:
        """
        Get user by phone number
        
        Args:
            phone: User phone number
            
        Returns:
            Optional[User]: User instance or None
        """
        try:
            return self.db.query(User).filter(User.phone == phone).first()
        except Exception as e:
            logger.error(f"Error getting user by phone {phone}: {e}")
            return None
    
    def search_users(self, search_term: str, limit: int = 10) -> List[User]:
        """
        Search users by name, email, or phone
        
        Args:
            search_term: Search term
            limit: Maximum results to return
            
        Returns:
            List[User]: List of matching users
        """
        try:
            return self.db.query(User).filter(
                or_(
                    User.first_name.ilike(f"%{search_term}%"),
                    User.last_name.ilike(f"%{search_term}%"),
                    User.email.ilike(f"%{search_term}%"),
                    User.phone.ilike(f"%{search_term}%")
                )
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error searching users with term {search_term}: {e}")
            return []
    
    def get_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get users by role
        
        Args:
            role: User role
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[User]: List of users with specified role
        """
        try:
            return self.db.query(User).filter(
                User.role == role
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting users by role {role}: {e}")
            return []
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get active users
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List[User]: List of active users
        """
        try:
            return self.db.query(User).filter(
                User.is_active == True
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            return []
    
    def activate_user(self, user_id: UUID) -> Optional[User]:
        """
        Activate user account
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: Updated user instance
        """
        try:
            user = self.get_by_id(user_id)
            if user:
                user.is_active = True
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"Activated user: {user.email}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error activating user {user_id}: {e}")
            return None
    
    def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """
        Deactivate user account
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: Updated user instance
        """
        try:
            user = self.get_by_id(user_id)
            if user:
                user.is_active = False
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"Deactivated user: {user.email}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deactivating user {user_id}: {e}")
            return None
    
    def update_last_login(self, user_id: UUID) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if updated successfully
        """
        try:
            user = self.get_by_id(user_id)
            if user:
                from datetime import datetime
                user.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Updated last login for user: {user.email}")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating last login for user {user_id}: {e}")
            return False
    
    def get_user_stats(self) -> Dict[str, Any]:
        """
        Get user statistics
        
        Returns:
            Dict[str, Any]: User statistics
        """
        try:
            total_users = self.count()
            active_users = self.count({"is_active": True})
            farmers = self.count({"role": "farmer"})
            experts = self.count({"role": "expert"})
            officers = self.count({"role": "agriculture_officer"})
            admins = self.count({"role": "admin"})
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users,
                "farmers": farmers,
                "experts": experts,
                "agriculture_officers": officers,
                "admins": admins
            }
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    def check_email_exists(self, email: str, exclude_user_id: Optional[UUID] = None) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            exclude_user_id: User ID to exclude from check
            
        Returns:
            bool: True if email exists
        """
        try:
            query = self.db.query(User).filter(User.email == email)
            if exclude_user_id:
                query = query.filter(User.id != exclude_user_id)
            return query.first() is not None
        except Exception as e:
            logger.error(f"Error checking email existence {email}: {e}")
            return False
    
    def check_firebase_uid_exists(self, firebase_uid: str, exclude_user_id: Optional[UUID] = None) -> bool:
        """
        Check if Firebase UID already exists
        
        Args:
            firebase_uid: Firebase UID to check
            exclude_user_id: User ID to exclude from check
            
        Returns:
            bool: True if Firebase UID exists
        """
        try:
            query = self.db.query(User).filter(User.firebase_uid == firebase_uid)
            if exclude_user_id:
                query = query.filter(User.id != exclude_user_id)
            return query.first() is not None
        except Exception as e:
            logger.error(f"Error checking Firebase UID existence {firebase_uid}: {e}")
            return False