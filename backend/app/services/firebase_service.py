"""
Firebase service for AGRO-BOT & AUTOMATION
"""

import json
import logging
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, auth, storage
from fastapi import HTTPException, status

from app.core.config import settings, get_firebase_config

logger = logging.getLogger(__name__)


class FirebaseService:
    """
    Firebase service for authentication and storage
    """
    
    def __init__(self):
        """Initialize Firebase service"""
        self._app = None
        self._bucket = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Get Firebase configuration
                firebase_config = get_firebase_config()
                
                # Create credentials
                cred = credentials.Certificate(firebase_config)
                
                # Initialize the app
                self._app = firebase_admin.initialize_app(cred, {
                    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                })
                
                logger.info("Firebase Admin SDK initialized successfully")
            else:
                # Use existing app
                self._app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
            
            # Initialize storage bucket
            if settings.FIREBASE_STORAGE_BUCKET:
                self._bucket = storage.bucket(settings.FIREBASE_STORAGE_BUCKET, app=self._app)
                logger.info(f"Firebase Storage bucket initialized: {settings.FIREBASE_STORAGE_BUCKET}")
        
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            # For development, we'll continue without Firebase
            logger.warning("Running without Firebase integration")
    
    async def verify_id_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token
        
        Args:
            id_token: Firebase ID token
            
        Returns:
            Optional[Dict[str, Any]]: Decoded token or None
        """
        try:
            if not self._app:
                # For development without Firebase
                logger.warning("Firebase not initialized, using mock verification")
                return self._mock_token_verification(id_token)
            
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token, app=self._app)
            
            logger.info(f"Token verified for user: {decoded_token.get('uid')}")
            return decoded_token
            
        except auth.InvalidIdTokenError:
            logger.error("Invalid Firebase ID token")
            return None
        except auth.ExpiredIdTokenError:
            logger.error("Expired Firebase ID token")
            return None
        except Exception as e:
            logger.error(f"Error verifying Firebase token: {e}")
            return None
    
    def _mock_token_verification(self, id_token: str) -> Dict[str, Any]:
        """
        Mock token verification for development
        
        Args:
            id_token: Firebase ID token
            
        Returns:
            Dict[str, Any]: Mock decoded token
        """
        # Simple mock for development
        if id_token.startswith("mock_"):
            return {
                "uid": f"mock_uid_{id_token[-10:]}",
                "email": "test@example.com",
                "name": "Test User",
                "email_verified": True,
                "iss": "https://securetoken.google.com/mock-project",
                "aud": "mock-project",
                "auth_time": 1234567890,
                "sub": f"mock_uid_{id_token[-10:]}",
                "iat": 1234567890,
                "exp": 1234567890 + 3600,
                "firebase": {
                    "identities": {
                        "email": ["test@example.com"]
                    },
                    "sign_in_provider": "password"
                }
            }
        return None
    
    async def get_user_by_uid(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user by Firebase UID
        
        Args:
            uid: Firebase user UID
            
        Returns:
            Optional[Dict[str, Any]]: User data or None
        """
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return None
            
            user_record = auth.get_user(uid, app=self._app)
            
            return {
                "uid": user_record.uid,
                "email": user_record.email,
                "email_verified": user_record.email_verified,
                "display_name": user_record.display_name,
                "photo_url": user_record.photo_url,
                "disabled": user_record.disabled,
                "provider_data": [
                    {
                        "uid": provider.uid,
                        "provider_id": provider.provider_id,
                        "email": provider.email,
                        "display_name": provider.display_name,
                        "photo_url": provider.photo_url
                    }
                    for provider in user_record.provider_data
                ]
            }
            
        except auth.UserNotFoundError:
            logger.error(f"Firebase user not found: {uid}")
            return None
        except Exception as e:
            logger.error(f"Error getting Firebase user {uid}: {e}")
            return None
    
    async def update_user_password(self, uid: str, new_password: str) -> bool:
        """
        Update user password
        
        Args:
            uid: Firebase user UID
            new_password: New password
            
        Returns:
            bool: True if updated successfully
        """
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return False
            
            auth.update_user(
                uid,
                password=new_password,
                app=self._app
            )
            
            logger.info(f"Password updated for user: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating password for user {uid}: {e}")
            return False
    
    async def send_password_reset_email(self, email: str) -> bool:
        """
        Send password reset email
        
        Args:
            email: User email
            
        Returns:
            bool: True if sent successfully
        """
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return False
            
            # Generate password reset link
            link = auth.generate_password_reset_link(email, app=self._app)
            
            # TODO: Implement actual email sending
            # For now, just log the link
            logger.info(f"Password reset link for {email}: {link}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending password reset email to {email}: {e}")
            return False
    
    async def refresh_token(self, refresh_token: str) -> Optional[str]:
        """
        Refresh Firebase token (placeholder)
        
        Args:
            refresh_token: Firebase refresh token
            
        Returns:
            Optional[str]: New ID token
        """
        try:
            # This needs to be implemented using Firebase REST API
            # As the Admin SDK doesn't provide token refresh functionality
            logger.warning("Token refresh not implemented")
            return None
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
    
    async def upload_file(self, file_data: bytes, file_name: str, content_type: str = None) -> Optional[str]:
        """
        Upload file to Firebase Storage
        
        Args:
            file_data: File data as bytes
            file_name: Name of the file
            content_type: MIME type of the file
            
        Returns:
            Optional[str]: Download URL or None
        """
        try:
            if not self._bucket:
                logger.warning("Firebase Storage not initialized")
                return None
            
            # Create blob
            blob = self._bucket.blob(file_name)
            
            # Upload file
            blob.upload_from_string(
                file_data,
                content_type=content_type or 'application/octet-stream'
            )
            
            # Make the file public (optional)
            blob.make_public()
            
            # Return public URL
            return blob.public_url
            
        except Exception as e:
            logger.error(f"Error uploading file {file_name}: {e}")
            return None
    
    async def delete_file(self, file_name: str) -> bool:
        """
        Delete file from Firebase Storage
        
        Args:
            file_name: Name of the file to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            if not self._bucket:
                logger.warning("Firebase Storage not initialized")
                return False
            
            # Delete blob
            blob = self._bucket.blob(file_name)
            blob.delete()
            
            logger.info(f"File deleted from storage: {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {file_name}: {e}")
            return False
    
    def get_storage_bucket(self):
        """Get Firebase Storage bucket"""
        return self._bucket
    
    def is_initialized(self) -> bool:
        """Check if Firebase is initialized"""
        return self._app is not None