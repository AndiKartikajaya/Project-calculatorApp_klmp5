"""
Service layer for calculator operations.
"""

import math
from typing import Dict, Any
import logging

from app.schemas.calculator import (
    BasicOperation, AdvancedOperation, ConversionRequest, 
    FinanceRequest, OperationType, CalculatorResponse
)

logger = logging.getLogger(__name__)


class CalculatorService:
    """
    Service class for calculator operations.
    
    Methods:
        calculate_basic: Perform basic calculations
        calculate_advanced: Perform advanced calculations
        convert_units: Convert between units
        calculate_finance: Perform financial calculations
        _create_expression_string: Create expression string for history
    """
    
    # Conversion factors
    CONVERSION_FACTORS = {
        "length": {
            "meter": 1,
            "kilometer": 1000,
            "centimeter": 0.01,
            "millimeter": 0.001,
            "mile": 1609.34,
            "yard": 0.9144,
            "foot": 0.3048,
            "inch": 0.0254
        },
        "weight": {
            "kilogram": 1,
            "gram": 0.001,
            "pound": 0.453592,
            "ounce": 0.0283495,
            "ton": 1000
        }
    }
    
    def calculate_basic(self, operation: BasicOperation) -> CalculatorResponse:
        """
        Perform basic mathematical operations.
        
        Args:
            operation (BasicOperation): Basic operation data
            
        Returns:
            CalculatorResponse: Calculation result
            
        Raises:
            ValueError: If operation is invalid
        """
        try:
            expression = ""
            result = 0.0
            
            if operation.operation == OperationType.ADDITION:
                result = operation.num1 + operation.num2
                expression = f"{operation.num1} + {operation.num2}"
            
            elif operation.operation == OperationType.SUBTRACTION:
                result = operation.num1 - operation.num2
                expression = f"{operation.num1} - {operation.num2}"
            
            elif operation.operation == OperationType.MULTIPLICATION:
                result = operation.num1 * operation.num2
                expression = f"{operation.num1} × {operation.num2}"
            
            elif operation.operation == OperationType.DIVISION:
                if operation.num2 == 0:
                    raise ValueError("Division by zero")
                result = operation.num1 / operation.num2
                expression = f"{operation.num1} ÷ {operation.num2}"
            
            elif operation.operation == OperationType.POWER:
                result = operation.num1 ** operation.num2
                expression = f"{operation.num1}^{operation.num2}"
            
            elif operation.operation == OperationType.PERCENTAGE:
                result = (operation.num1 * operation.num2) / 100
                expression = f"{operation.num1}% of {operation.num2}"
            
            else:
                raise ValueError(f"Unsupported basic operation: {operation.operation}")
            
            return CalculatorResponse(
                result=result,
                expression=expression,
                operation_type=operation.operation
            )
            
        except Exception as e:
            logger.error(f"Basic calculation error: {str(e)}")
            raise
    
    def calculate_advanced(self, operation: AdvancedOperation) -> CalculatorResponse:
        """
        Perform advanced mathematical operations.
        
        Args:
            operation (AdvancedOperation): Advanced operation data
            
        Returns:
            CalculatorResponse: Calculation result
            
        Raises:
            ValueError: If operation is invalid
        """
        try:
            value = operation.value
            expression = ""
            result = 0.0
            
            # Convert to radians if needed for trigonometric functions
            if operation.angle_unit == "degrees" and operation.operation in [
                OperationType.SIN, OperationType.COS, OperationType.TAN
            ]:
                value = math.radians(value)
                angle_suffix = "°"
            else:
                angle_suffix = " rad" if operation.operation in [
                    OperationType.SIN, OperationType.COS, OperationType.TAN
                ] else ""
            
            if operation.operation == OperationType.SQUARE_ROOT:
                if value < 0:
                    raise ValueError("Square root of negative number")
                result = math.sqrt(value)
                expression = f"√{value}"
            
            elif operation.operation == OperationType.SIN:
                result = math.sin(value)
                expression = f"sin({operation.value}{angle_suffix})"
            
            elif operation.operation == OperationType.COS:
                result = math.cos(value)
                expression = f"cos({operation.value}{angle_suffix})"
            
            elif operation.operation == OperationType.TAN:
                result = math.tan(value)
                expression = f"tan({operation.value}{angle_suffix})"
            
            elif operation.operation == OperationType.LOG:
                result = math.log10(value)
                expression = f"log₁₀({value})"
            
            elif operation.operation == OperationType.LN:
                result = math.log(value)
                expression = f"ln({value})"
            
            else:
                raise ValueError(f"Unsupported advanced operation: {operation.operation}")
            
            return CalculatorResponse(
                result=result,
                expression=expression,
                operation_type=operation.operation
            )
            
        except Exception as e:
            logger.error(f"Advanced calculation error: {str(e)}")
            raise
    
    def convert_units(self, conversion: ConversionRequest) -> CalculatorResponse:
        """
        Convert between different units.
        
        Args:
            conversion (ConversionRequest): Conversion data
            
        Returns:
            CalculatorResponse: Conversion result
            
        Raises:
            ValueError: If conversion type or units are invalid
        """
        try:
            if conversion.conversion_type not in self.CONVERSION_FACTORS:
                raise ValueError(f"Unsupported conversion type: {conversion.conversion_type}")
            
            factors = self.CONVERSION_FACTORS[conversion.conversion_type]
            
            if conversion.from_unit not in factors or conversion.to_unit not in factors:
                raise ValueError(f"Invalid units for {conversion.conversion_type} conversion")
            
            # Convert to base unit first, then to target unit
            value_in_base = conversion.value * factors[conversion.from_unit]
            result = value_in_base / factors[conversion.to_unit]
            
            # Special handling for temperature
            if conversion.conversion_type == "temperature":
                result = self._convert_temperature(
                    conversion.value, conversion.from_unit, conversion.to_unit
                )
                expression = f"{conversion.value} {conversion.from_unit} → {conversion.to_unit}"
            else:
                expression = f"{conversion.value} {conversion.from_unit} = ? {conversion.to_unit}"
            
            return CalculatorResponse(
                result=result,
                expression=expression,
                operation_type=OperationType.CONVERSION
            )
            
        except Exception as e:
            logger.error(f"Unit conversion error: {str(e)}")
            raise
    
    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert temperature between units.
        
        Args:
            value (float): Temperature value
            from_unit (str): Source temperature unit
            to_unit (str): Target temperature unit
            
        Returns:
            float: Converted temperature
        """
        # Convert to Celsius first
        if from_unit == "celsius":
            celsius = value
        elif from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {from_unit}")
        
        # Convert from Celsius to target unit
        if to_unit == "celsius":
            return celsius
        elif to_unit == "fahrenheit":
            return (celsius * 9/5) + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {to_unit}")
    
    def calculate_finance(self, finance: FinanceRequest) -> CalculatorResponse:
        """
        Perform financial calculations.
        
        Args:
            finance (FinanceRequest): Financial calculation data
            
        Returns:
            CalculatorResponse: Calculation result
        """
        try:
            principal = finance.principal
            rate = finance.rate / 100  # Convert percentage to decimal
            time = finance.time
            result = 0.0
            expression = ""
            
            if finance.operation == "simple_interest":
                result = principal * rate * time
                expression = f"SI: P={principal}, R={finance.rate}%, T={time}"
            
            elif finance.operation == "compound_interest":
                # Assuming annual compounding
                result = principal * ((1 + rate) ** time - 1)
                expression = f"CI: P={principal}, R={finance.rate}%, T={time}"
            
            elif finance.operation == "loan_payment":
                # Monthly payment calculation
                monthly_rate = rate / 12
                n_payments = time * 12
                if monthly_rate == 0:
                    result = principal / n_payments
                else:
                    result = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / \
                             ((1 + monthly_rate) ** n_payments - 1)
                expression = f"Loan: P={principal}, R={finance.rate}% p.a., T={time} years"
            
            else:
                raise ValueError(f"Unsupported financial operation: {finance.operation}")
            
            return CalculatorResponse(
                result=round(result, 2),
                expression=expression,
                operation_type=OperationType.FINANCE
            )
            
        except Exception as e:
            logger.error(f"Financial calculation error: {str(e)}")
            raise