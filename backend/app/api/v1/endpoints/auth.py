"""
Authentication endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Any, Dict

from app.core.database import get_db
from app.core.security import verify_firebase_token, create_access_token, get_current_user
from app.models.user import User
from app.models.farmer import Farmer
from app.schemas.auth import (
    UserLogin, UserRegister, Token, UserResponse,
    FarmerRegisterData, LoginResponse
)
from app.services.firebase_service import FirebaseService
from app.services.user_service import UserService
from app.services.farmer_service import FarmerService
from app.utils.logger import get_logger

# Setup
router = APIRouter()
security = HTTPBearer()
logger = get_logger(__name__)


@router.post("/register", response_model=LoginResponse)
async def register_user(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user with Firebase Authentication
    
    Args:
        user_data: User registration data
        request: HTTP request object
        db: Database session
        
    Returns:
        LoginResponse: User data and access token
    """
    try:
        # Verify Firebase ID token
        firebase_service = request.app.state.firebase
        decoded_token = await firebase_service.verify_id_token(user_data.firebase_id_token)
        
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Firebase ID token"
            )
        
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email')
        
        # Check if user already exists
        user_service = UserService(db)
        existing_user = user_service.get_by_firebase_uid(firebase_uid)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        
        # Create new user
        user_create_data = {
            "firebase_uid": firebase_uid,
            "email": email or user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone": user_data.phone,
            "role": user_data.role or "farmer",
            "language_preference": user_data.language_preference or "en"
        }
        
        user = user_service.create(user_create_data)
        
        # Create farmer profile if role is farmer
        if user.role == "farmer" and hasattr(user_data, 'farmer_data') and user_data.farmer_data:
            farmer_service = FarmerService(db)
            farmer_data = user_data.farmer_data.dict()
            farmer_data['user_id'] = user.id
            farmer_service.create(farmer_data)
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": str(user.id), "firebase_uid": firebase_uid}
        )
        
        logger.info(f"New user registered: {user.email}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user),
            message="User registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=LoginResponse)
async def login_user(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """
    Authenticate user with Firebase ID token
    
    Args:
        user_data: User login data
        request: HTTP request object  
        db: Database session
        
    Returns:
        LoginResponse: User data and access token
    """
    try:
        # Verify Firebase ID token
        firebase_service = request.app.state.firebase
        decoded_token = await firebase_service.verify_id_token(user_data.firebase_id_token)
        
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Firebase ID token"
            )
        
        firebase_uid = decoded_token['uid']
        
        # Get user from database
        user_service = UserService(db)
        user = user_service.get_by_firebase_uid(firebase_uid)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please register first."
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": str(user.id), "firebase_uid": firebase_uid}
        )
        
        # Update last login (optional)
        user_service.update_last_login(user.id)
        
        logger.info(f"User logged in: {user.email}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer", 
            user=UserResponse.from_orm(user),
            message="Login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/verify-token", response_model=UserResponse)
async def verify_token(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Verify JWT access token and return current user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user data
    """
    return UserResponse.from_orm(current_user)


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_data: dict,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using Firebase refresh token
    
    Args:
        refresh_data: Refresh token data
        request: HTTP request object
        db: Database session
        
    Returns:
        Token: New access token
    """
    try:
        firebase_service = request.app.state.firebase
        
        # Refresh Firebase token
        new_id_token = await firebase_service.refresh_token(
            refresh_data.get('refresh_token')
        )
        
        if not new_id_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Verify new ID token
        decoded_token = await firebase_service.verify_id_token(new_id_token)
        firebase_uid = decoded_token['uid']
        
        # Get user
        user_service = UserService(db)
        user = user_service.get_by_firebase_uid(firebase_uid)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate new access token
        access_token = create_access_token(
            data={"sub": str(user.id), "firebase_uid": firebase_uid}
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Logout user (client-side token removal)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    logger.info(f"User logged out: {current_user.email}")
    
    return {
        "message": "Logout successful",
        "detail": "Please remove the access token from client storage"
    }


@router.post("/change-password")
async def change_password(
    password_data: dict,
    current_user: User = Depends(get_current_user),
    request: Request = None
) -> Any:
    """
    Change user password (handled by Firebase)
    
    Args:
        password_data: Password change data
        current_user: Current authenticated user
        request: HTTP request object
        
    Returns:
        dict: Success message
    """
    try:
        firebase_service = request.app.state.firebase
        
        # Update password in Firebase
        await firebase_service.update_user_password(
            current_user.firebase_uid,
            password_data.get('new_password')
        )
        
        logger.info(f"Password changed for user: {current_user.email}")
        
        return {"message": "Password changed successfully"}
        
    except Exception as e:
        logger.error(f"Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.post("/forgot-password")
async def forgot_password(
    email_data: dict,
    request: Request
) -> Any:
    """
    Send password reset email
    
    Args:
        email_data: Email address
        request: HTTP request object
        
    Returns:
        dict: Success message
    """
    try:
        firebase_service = request.app.state.firebase
        email = email_data.get('email')
        
        # Send password reset email via Firebase
        await firebase_service.send_password_reset_email(email)
        
        logger.info(f"Password reset email sent to: {email}")
        
        return {"message": "Password reset email sent successfully"}
        
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user profile
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: User profile data
    """
    return UserResponse.from_orm(current_user)


@router.put("/profile", response_model=UserResponse) 
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update user profile
    
    Args:
        profile_data: Profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        UserResponse: Updated user profile
    """
    try:
        user_service = UserService(db)
        updated_user = user_service.update(current_user.id, profile_data)
        
        logger.info(f"Profile updated for user: {current_user.email}")
        
        return UserResponse.from_orm(updated_user)
        
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )