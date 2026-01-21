"""
Calculator API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.schemas.calculator import (
    BasicOperation, AdvancedOperation, ConversionRequest, 
    FinanceRequest, CalculatorResponse
)
from app.schemas.history import HistoryResponse
from app.services.calculator_service import CalculatorService
from app.services.history_service import HistoryService
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.history_repository import HistoryRepository

router = APIRouter(prefix="/calculator", tags=["calculator"])
http_bearer = HTTPBearer(description="Access token using Bearer scheme")


def get_current_user_id(credentials = Depends(http_bearer), db: Session = Depends(get_db)) -> int:
    """
    Dependency to get current user ID from JWT token (Bearer scheme).
    
    Args:
        credentials: HTTPAuthorizationCredentials from HTTPBearer
        db (Session): Database session
        
    Returns:
        int: Current user ID
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        # Extract token from HTTPAuthorizationCredentials object
        token = credentials.credentials
            
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        token_data = auth_service.verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        return token_data.user_id
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )


@router.post("/basic", response_model=Dict[str, Any])
async def calculate_basic(
    operation: BasicOperation,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Perform basic mathematical operation.
    
    Args:
        operation (BasicOperation): Basic operation data
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Calculation result and history record
        
    Raises:
        HTTPException: If calculation fails
    """
    try:
        # Perform calculation
        calculator_service = CalculatorService()
        result = calculator_service.calculate_basic(operation)
        
        # Save to history
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        history_record = history_service.add_to_history(
            user_id=user_id,
            operation_type=result.operation_type.value,
            expression=result.expression,
            result=str(result.result)
        )
        
        return {
            "result": result.result,
            "expression": result.expression,
            "operation": result.operation_type.value,
            "history_id": history_record.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


@router.post("/advanced", response_model=Dict[str, Any])
async def calculate_advanced(
    operation: AdvancedOperation,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Perform advanced mathematical operation.
    
    Args:
        operation (AdvancedOperation): Advanced operation data
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Calculation result and history record
        
    Raises:
        HTTPException: If calculation fails
    """
    try:
        # Perform calculation
        calculator_service = CalculatorService()
        result = calculator_service.calculate_advanced(operation)
        
        # Save to history
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        history_record = history_service.add_to_history(
            user_id=user_id,
            operation_type=result.operation_type.value,
            expression=result.expression,
            result=str(result.result)
        )
        
        return {
            "result": result.result,
            "expression": result.expression,
            "operation": result.operation_type.value,
            "history_id": history_record.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


@router.post("/convert", response_model=Dict[str, Any])
async def convert_units(
    conversion: ConversionRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Convert between different units.
    
    Args:
        conversion (ConversionRequest): Conversion data
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Conversion result and history record
        
    Raises:
        HTTPException: If conversion fails
    """
    try:
        # Perform conversion
        calculator_service = CalculatorService()
        result = calculator_service.convert_units(conversion)
        
        # Save to history
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        history_record = history_service.add_to_history(
            user_id=user_id,
            operation_type=result.operation_type.value,
            expression=result.expression,
            result=f"{result.result:.4f} {conversion.to_unit}"
        )
        
        return {
            "result": result.result,
            "from_unit": conversion.from_unit,
            "to_unit": conversion.to_unit,
            "converted_value": f"{result.result:.4f} {conversion.to_unit}",
            "history_id": history_record.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversion failed: {str(e)}"
        )


@router.post("/finance", response_model=Dict[str, Any])
async def calculate_finance(
    finance: FinanceRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Perform financial calculations.
    
    Args:
        finance (FinanceRequest): Financial calculation data
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Calculation result and history record
        
    Raises:
        HTTPException: If calculation fails
    """
    try:
        # Perform financial calculation
        calculator_service = CalculatorService()
        result = calculator_service.calculate_finance(finance)
        
        # Save to history
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        history_record = history_service.add_to_history(
            user_id=user_id,
            operation_type=result.operation_type.value,
            expression=result.expression,
            result=f"{result.result:.2f}"
        )
        
        return {
            "result": result.result,
            "operation": finance.operation,
            "expression": result.expression,
            "history_id": history_record.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Financial calculation failed: {str(e)}"
        )


@router.get("/operations")
async def get_available_operations() -> Dict[str, Any]:
    """
    Get list of available calculator operations.
    
    Returns:
        Dict[str, Any]: Available operations categorized
    """
    return {
        "basic_operations": [
            {"id": "addition", "name": "Addition", "symbol": "+", "inputs": 2},
            {"id": "subtraction", "name": "Subtraction", "symbol": "-", "inputs": 2},
            {"id": "multiplication", "name": "Multiplication", "symbol": "×", "inputs": 2},
            {"id": "division", "name": "Division", "symbol": "÷", "inputs": 2},
            {"id": "power", "name": "Power", "symbol": "^", "inputs": 2},
            {"id": "percentage", "name": "Percentage", "symbol": "%", "inputs": 2}
        ],
        "advanced_operations": [
            {"id": "square_root", "name": "Square Root", "symbol": "√", "inputs": 1},
            {"id": "sin", "name": "Sine", "symbol": "sin", "inputs": 1},
            {"id": "cos", "name": "Cosine", "symbol": "cos", "inputs": 1},
            {"id": "tan", "name": "Tangent", "symbol": "tan", "inputs": 1},
            {"id": "log", "name": "Logarithm (base 10)", "symbol": "log", "inputs": 1},
            {"id": "ln", "name": "Natural Logarithm", "symbol": "ln", "inputs": 1}
        ],
        "conversions": {
            "length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
            "weight": ["kilogram", "gram", "pound", "ounce", "ton"],
            "temperature": ["celsius", "fahrenheit", "kelvin"]
        },
        "finance_operations": [
            {"id": "simple_interest", "name": "Simple Interest", "inputs": 3},
            {"id": "compound_interest", "name": "Compound Interest", "inputs": 3},
            {"id": "loan_payment", "name": "Loan Monthly Payment", "inputs": 3}
        ]
    }