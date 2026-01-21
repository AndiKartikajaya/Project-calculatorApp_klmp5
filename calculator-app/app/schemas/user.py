"""
Pydantic schemas for user-related operations.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for user data."""
    username: str = Field(..., min_length=3, max_length=50, 
                         description="Username must be 3-50 characters")
    email: str = Field(..., description="Email address")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Simple email validation."""
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Invalid email format')
        return v.lower()


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100,
                         description="Password must be at least 8 characters")
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    username: Optional[str] = None
    email: Optional[str] = None
    password: str = Field(...)
    
    @model_validator(mode='after')
    def check_credentials(self):
        """Ensure either username or email is provided."""
        if self.username is None and self.email is None:
            raise ValueError('Either username or email must be provided')
        return self


class UserResponse(UserBase):
    """Schema for user response (without sensitive data)."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None
    username: Optional[str] = None