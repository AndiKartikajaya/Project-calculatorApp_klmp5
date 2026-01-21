"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
http_bearer = HTTPBearer(description="Access token using Bearer scheme")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user.
    
    Args:
        user_data (UserCreate): User registration data
        db (Session): Database session
        
    Returns:
        UserResponse: Created user data
        
    Raises:
        HTTPException: If username or email already exists
    """
    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        # Check if user already exists
        if user_repo.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if user_repo.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = auth_service.get_password_hash(user_data.password)
        user = user_repo.create_user(user_data, hashed_password)
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: UserLogin,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    User login endpoint.
    
    Args:
        form_data (UserLogin): Login credentials
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Access token and user data
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        # Determine login method
        if form_data.username:
            auth_result = auth_service.authenticate_user(
                username=form_data.username,
                password=form_data.password
            )
        else:
            # Find username from email
            user = user_repo.get_user_by_email(form_data.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            auth_result = auth_service.authenticate_user(
                username=user.username,
                password=form_data.password
            )
        
        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return auth_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials = Depends(http_bearer),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get current user information.
    
    Args:
        credentials: HTTPAuthorizationCredentials from HTTPBearer
        db (Session): Database session
        
    Returns:
        UserResponse: Current user data
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Extract token from HTTPAuthorizationCredentials object
        token = credentials.credentials
            
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        # Verify token
        token_data = auth_service.verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Get user
        user = user_repo.get_user_by_id(token_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )


@router.post("/logout")
async def logout() -> Dict[str, str]:
    """
    User logout endpoint.
    
    Note: Since we're using stateless JWT tokens, logout is handled client-side
    by discarding the token. This endpoint is for API consistency.
    
    Returns:
        Dict[str, str]: Logout message
    """
    return {"message": "Successfully logged out. Please discard your token."}