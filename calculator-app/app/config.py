"""
Configuration module for MathHub Calculator application.
Handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./calculator.db"
    DATABASE_TEST_URL: str = "sqlite:///./test.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Calculator API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()