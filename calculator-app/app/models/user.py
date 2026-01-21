"""
User model for database.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    User model representing registered users.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username
        email (str): Unique email address
        password_hash (str): Hashed password
        created_at (datetime): Account creation timestamp
        calculations (relationship): One-to-many relationship with CalculationHistory
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with calculation history
    calculations = relationship("CalculationHistory", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"