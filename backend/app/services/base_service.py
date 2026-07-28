"""
Base service class for AGRO-BOT & AUTOMATION
Provides common CRUD operations for all services
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
import logging

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

logger = logging.getLogger(__name__)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base service with default CRUD operations
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize base service
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: Union[UUID, str]) -> Optional[ModelType]:
        """
        Get record by ID
        
        Args:
            id: Record ID
            
        Returns:
            Optional[ModelType]: Model instance or None
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by ID {id}: {e}")
            return None
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and filtering
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Filter conditions
            order_by: Field to order by
            
        Returns:
            List[ModelType]: List of model instances
        """
        try:
            query = self.db.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        if isinstance(value, list):
                            query = query.filter(getattr(self.model, field).in_(value))
                        else:
                            query = query.filter(getattr(self.model, field) == value)
            
            # Apply ordering
            if order_by and hasattr(self.model, order_by):
                query = query.order_by(getattr(self.model, order_by))
            
            return query.offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting multiple {self.model.__name__}: {e}")
            return []
    
    def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        Create new record
        
        Args:
            obj_in: Data to create record
            
        Returns:
            ModelType: Created model instance
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            # Convert to dict if it's a Pydantic model
            if hasattr(obj_in, 'dict'):
                obj_data = obj_in.dict()
            else:
                obj_data = obj_in
                
            # Create model instance
            db_obj = self.model(**obj_data)
            
            # Add to session and commit
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            
            logger.info(f"Created {self.model.__name__} with ID: {db_obj.id}")
            return db_obj
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating {self.model.__name__.lower()}"
            )
    
    def update(
        self, 
        id: Union[UUID, str], 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """
        Update existing record
        
        Args:
            id: Record ID
            obj_in: Data to update record
            
        Returns:
            Optional[ModelType]: Updated model instance
            
        Raises:
            HTTPException: If update fails
        """
        try:
            # Get existing record
            db_obj = self.get_by_id(id)
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found"
                )
            
            # Convert to dict if it's a Pydantic model
            if hasattr(obj_in, 'dict'):
                obj_data = obj_in.dict(exclude_unset=True)
            else:
                obj_data = obj_in
            
            # Update fields
            for field, value in obj_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            # Commit changes
            self.db.commit()
            self.db.refresh(db_obj)
            
            logger.info(f"Updated {self.model.__name__} with ID: {id}")
            return db_obj
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating {self.model.__name__.lower()}"
            )
    
    def delete(self, id: Union[UUID, str]) -> bool:
        """
        Delete record by ID
        
        Args:
            id: Record ID
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            HTTPException: If deletion fails
        """
        try:
            # Get existing record
            db_obj = self.get_by_id(id)
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found"
                )
            
            # Delete record
            self.db.delete(db_obj)
            self.db.commit()
            
            logger.info(f"Deleted {self.model.__name__} with ID: {id}")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting {self.model.__name__.lower()}"
            )
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filtering
        
        Args:
            filters: Filter conditions
            
        Returns:
            int: Number of records
        """
        try:
            query = self.db.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.count()
            
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            return 0
    
    def exists(self, id: Union[UUID, str]) -> bool:
        """
        Check if record exists
        
        Args:
            id: Record ID
            
        Returns:
            bool: True if record exists
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).first() is not None
        except Exception as e:
            logger.error(f"Error checking {self.model.__name__} existence {id}: {e}")
            return False