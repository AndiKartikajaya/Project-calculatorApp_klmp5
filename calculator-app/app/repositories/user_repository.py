"""
Repository layer for user database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
import logging

from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


class UserRepository:
    """
    Repository class for user-related database operations.
    
    Methods:
        create_user: Create new user
        get_user_by_id: Get user by ID
        get_user_by_username: Get user by username
        get_user_by_email: Get user by email
        authenticate_user: Authenticate user credentials
        update_user: Update user information
        delete_user: Delete user
        get_all_users: Get all users (admin only)
    """
    
    def __init__(self, db: Session):
        """
        Initialize UserRepository.
        
        Args:
            db (Session): Database session
        """
        self.db = db
    
    def create_user(self, user_data: UserCreate, hashed_password: str) -> Optional[User]:
        """
        Create a new user in the database.
        
        Args:
            user_data (UserCreate): User creation data
            hashed_password (str): Hashed password
            
        Returns:
            Optional[User]: Created user or None if creation failed
            
        Raises:
            IntegrityError: If username or email already exists
        """
        try:
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                password_hash=hashed_password
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"User created: {user_data.username}")
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error creating user {user_data.username}: {str(e)}")
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Unexpected error creating user: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Optional[User]: User object or None if not found
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username (str): Username
            
        Returns:
            Optional[User]: User object or None if not found
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email (str): Email address
            
        Returns:
            Optional[User]: User object or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, username: Optional[str] = None, 
                         email: Optional[str] = None, 
                         password_hash: str = None) -> Optional[User]:
        """
        Authenticate user with username/email and password hash.
        
        Args:
            username (Optional[str]): Username
            email (Optional[str]): Email address
            password_hash (str): Hashed password to verify
            
        Returns:
            Optional[User]: Authenticated user or None
        """
        user = None
        
        if username:
            user = self.get_user_by_username(username)
        elif email:
            user = self.get_user_by_email(email)
        
        if user and user.password_hash == password_hash:
            return user
        
        return None
    
    def update_user(self, user_id: int, update_data: dict) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id (int): User ID to update
            update_data (dict): Dictionary of fields to update
            
        Returns:
            Optional[User]: Updated user or None if not found
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User updated: {user_id}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id (int): User ID to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            self.db.delete(user)
            self.db.commit()
            logger.info(f"User deleted: {user_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users (for admin purposes).
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            
        Returns:
            List[User]: List of users
        """
        return self.db.query(User).offset(skip).limit(limit).all()