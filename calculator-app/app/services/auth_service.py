"""
Service layer for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Optional
import logging

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.schemas.user import TokenData
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service class for authentication operations.
    
    Methods:
        verify_password: Verify plain password against hash
        get_password_hash: Hash password
        create_access_token: Create JWT access token
        verify_token: Verify and decode JWT token
        authenticate_user: Authenticate user credentials
        get_current_user: Get current user from token
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Initialize AuthService.
        
        Args:
            user_repository (UserRepository): User repository instance
        """
        self.user_repository = user_repository
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify plain password against hashed password.
        
        Args:
            plain_password (str): Plain text password
            hashed_password (str): Hashed password
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate password hash.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            data (dict): Token payload data
            expires_delta (Optional[timedelta]): Token expiration time
            
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
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify and decode JWT token.
        
        Args:
            token (str): JWT token
            
        Returns:
            Optional[TokenData]: Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: Optional[int] = payload.get("sub")
            username: Optional[str] = payload.get("username")
            
            if user_id is None or username is None:
                return None
            
            return TokenData(user_id=user_id, username=username)
        except JWTError as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """
        Authenticate user with username and password.
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            Optional[dict]: User data if authenticated, None otherwise
        """
        try:
            user = self.user_repository.get_user_by_username(username)
            if not user:
                # Try email
                user = self.user_repository.get_user_by_email(username)
            
            if not user or not self.verify_password(password, user.password_hash):
                return None
            
            # Create token
            access_token = self.create_access_token(
                data={"sub": str(user.id), "username": user.username}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # <-- TAMBAHKAN
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {str(e)}")
            return None