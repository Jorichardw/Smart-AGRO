"""
User endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user, get_admin_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserList, UserStats, UserSearch
from app.services.user_service import UserService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return UserResponse.from_attributes(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    try:
        user_service = UserService(db)
        updated_user = user_service.update(current_user.id, user_update.dict(exclude_unset=True))
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User profile updated: {current_user.email}")
        return UserResponse.from_attributes(updated_user)
        
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user profile"
        )


@router.get("/", response_model=UserList)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records"),
    role: Optional[str] = Query(None, description="Filter by user role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get list of users (Admin only)"""
    try:
        user_service = UserService(db)
        
        # Build filters
        filters = {}
        if role:
            filters['role'] = role
        if is_active is not None:
            filters['is_active'] = is_active
        
        # Get users
        users = user_service.get_multi(skip=skip, limit=limit, filters=filters)
        total = user_service.count(filters)
        
        # Calculate pagination
        pages = (total + limit - 1) // limit
        
        return UserList(
            users=[UserResponse.from_attributes(user) for user in users],
            total=total,
            page=(skip // limit) + 1,
            size=limit,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (Admin only)"""
    try:
        user_service = UserService(db)
        user = user_service.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_attributes(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update user (Admin only)"""
    try:
        user_service = UserService(db)
        updated_user = user_service.update(user_id, user_update.dict(exclude_unset=True))
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User updated by admin: {user_id}")
        return UserResponse.from_attributes(updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )


@router.post("/{user_id}/activate")
async def activate_user(
    user_id: UUID,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Activate user account (Admin only)"""
    try:
        user_service = UserService(db)
        user = user_service.activate_user(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User activated by admin: {user_id}")
        return {"message": "User activated successfully", "user_id": str(user_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating user"
        )


@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Deactivate user account (Admin only)"""
    try:
        user_service = UserService(db)
        user = user_service.deactivate_user(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User deactivated by admin: {user_id}")
        return {"message": "User deactivated successfully", "user_id": str(user_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating user"
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (Admin only)"""
    try:
        user_service = UserService(db)
        
        # Check if user exists
        user = user_service.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prevent admin from deleting themselves
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Delete user
        success = user_service.delete(user_id)
        
        if success:
            logger.info(f"User deleted by admin: {user_id}")
            return {"message": "User deleted successfully", "user_id": str(user_id)}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting user"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )


@router.get("/search/", response_model=List[UserResponse])
async def search_users(
    search: UserSearch,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Search users (Admin only)"""
    try:
        user_service = UserService(db)
        users = user_service.search_users(search.search_term, search.limit)
        
        return [UserResponse.from_attributes(user) for user in users]
        
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching users"
        )


@router.get("/stats/overview", response_model=UserStats)
async def get_user_statistics(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user statistics (Admin only)"""
    try:
        user_service = UserService(db)
        stats = user_service.get_user_stats()
        
        return UserStats(**stats)
        
    except Exception as e:
        logger.error(f"Error getting user statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )