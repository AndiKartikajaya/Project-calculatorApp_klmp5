"""
Pydantic schemas for calculator operations.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, Union
from enum import Enum


class OperationType(str, Enum):
    """Enum for operation types."""
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    POWER = "power"
    SQUARE_ROOT = "square_root"
    PERCENTAGE = "percentage"
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    LOG = "log"
    LN = "ln"
    CONVERSION = "conversion"
    FINANCE = "finance"


class BasicOperation(BaseModel):
    """
    Schema for basic calculator operations.
    
    Attributes:
        num1 (float): First number
        num2 (float): Second number (for binary operations)
        operation (OperationType): Type of operation
    """
    num1: float = Field(..., description="First number")
    num2: Optional[float] = Field(None, description="Second number (for binary operations)")
    operation: OperationType = Field(..., description="Type of operation")
    
    @field_validator('num2')
    @classmethod
    def validate_num2_for_division(cls, v: Optional[float], info) -> Optional[float]:
        """Validate num2 for division operation."""
        operation = info.data.get('operation')
        if operation == OperationType.DIVISION and v == 0:
            raise ValueError('Division by zero is not allowed')
        return v


class AdvancedOperation(BaseModel):
    """
    Schema for advanced calculator operations.
    
    Attributes:
        value (float): Input value
        operation (OperationType): Type of operation
        angle_unit (str): Unit for trigonometric functions (radians/degrees)
    """
    value: float = Field(..., description="Input value")
    operation: OperationType = Field(..., description="Type of operation")
    angle_unit: Optional[str] = Field("radians", description="Angle unit: radians or degrees")
    
    @field_validator('angle_unit')
    @classmethod
    def validate_angle_unit(cls, v: str) -> str:
        """Validate angle unit."""
        if v not in ["radians", "degrees"]:
            raise ValueError('Angle unit must be either "radians" or "degrees"')
        return v
    
    @field_validator('value')
    @classmethod
    def validate_value_for_functions(cls, v: float, info) -> float:
        """Validate value for specific functions."""
        operation = info.data.get('operation')
        
        if operation == OperationType.LOG and v <= 0:
            raise ValueError('Logarithm requires positive value')
        elif operation == OperationType.LN and v <= 0:
            raise ValueError('Natural logarithm requires positive value')
        elif operation == OperationType.SQUARE_ROOT and v < 0:
            raise ValueError('Square root requires non-negative value')
        
        return v


class ConversionRequest(BaseModel):
    """
    Schema for unit conversion operations.
    
    Attributes:
        value (float): Value to convert
        from_unit (str): Source unit
        to_unit (str): Target unit
        conversion_type (str): Type of conversion (length, weight, temperature)
    """
    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")
    conversion_type: Literal["length", "weight", "temperature"] = Field(
        ..., description="Type of conversion"
    )


class FinanceRequest(BaseModel):
    """
    Schema for financial calculations.
    
    Attributes:
        principal (float): Principal amount
        rate (float): Interest rate (percentage)
        time (float): Time period
        operation (str): Type of financial calculation
    """
    principal: float = Field(..., gt=0, description="Principal amount")
    rate: float = Field(..., ge=0, description="Interest rate in percentage")
    time: float = Field(..., gt=0, description="Time period")
    operation: Literal["simple_interest", "compound_interest", "loan_payment"] = Field(
        ..., description="Type of financial calculation"
    )


class CalculatorResponse(BaseModel):
    """
    Schema for calculator response.
    
    Attributes:
        result (Union[float, str]): Calculation result
        expression (str): Mathematical expression
        operation_type (OperationType): Type of operation performed
    """
    result: Union[float, str]
    expression: str
    operation_type: OperationType
