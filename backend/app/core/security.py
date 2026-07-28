"""
Security utilities for AGRO-BOT & AUTOMATION
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.services.user_service import UserService

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Data to encode in token
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token to verify
        
    Returns:
        Optional[dict]: Decoded token data or None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except PyJWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


async def verify_firebase_token(token: str) -> Optional[dict]:
    """
    Verify Firebase ID token (placeholder)
    
    Args:
        token: Firebase ID token
        
    Returns:
        Optional[dict]: Decoded token data
    """
    # TODO: Implement actual Firebase token verification
    # This is a placeholder for Firebase Admin SDK integration
    try:
        # firebase_admin.auth.verify_id_token(token)
        # For now, return mock data for development
        return {"uid": "mock_firebase_uid", "email": "test@example.com"}
    except Exception:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extract token from credentials
        token = credentials.credentials
        
        # Verify and decode token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        
        # Get user ID from payload
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get user from database
        user_service = UserService(db)
        user = user_service.get_by_id(user_id)
        
        if user is None:
            raise credentials_exception
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )
            
        return user
        
    except PyJWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_roles(allowed_roles: list):
    """
    Decorator to require specific user roles
    
    Args:
        allowed_roles: List of allowed user roles
        
    Returns:
        Function: Dependency function
    """
    def role_dependency(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for user role"
            )
        return current_user
    
    return role_dependency


# Convenience functions for role-based access
get_admin_user = require_roles(["admin"])
get_farmer_user = require_roles(["farmer", "admin"])
get_expert_user = require_roles(["expert", "admin"])
get_officer_user = require_roles(["agriculture_officer", "admin"])