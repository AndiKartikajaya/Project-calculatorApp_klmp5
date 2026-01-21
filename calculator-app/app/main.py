"""
Main FastAPI application module.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import uvicorn

from app.database import engine, Base
from app.api import auth, calculator, history
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="MathHub Calculator API - Advanced calculator with history tracking",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api")
app.include_router(calculator.router, prefix="/api")
app.include_router(history.router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors and return user-friendly messages.
    
    Args:
        request (Request): FastAPI request
        exc (RequestValidationError): Validation exception
        
    Returns:
        JSONResponse: Error response
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation failed",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions.
    
    Args:
        request (Request): FastAPI request
        exc (Exception): Exception
        
    Returns:
        JSONResponse: Error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/api/docs",
        "endpoints": {
            "auth": "/api/auth",
            "calculator": "/api/calculator",
            "history": "/api/history"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "timestamp": "current_time"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )