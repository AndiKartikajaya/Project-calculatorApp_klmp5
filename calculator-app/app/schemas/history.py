"""
Pydantic schemas for calculation history.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from app.schemas.calculator import OperationType


class HistoryResponse(BaseModel):
    """
    Schema for calculation history response.
    
    Attributes:
        id (int): History record ID
        operation_type (OperationType): Type of operation
        expression (str): Mathematical expression
        result (str): Calculation result
        created_at (datetime): Timestamp
    """
    id: int
    operation_type: OperationType
    expression: str
    result: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class HistoryFilter(BaseModel):
    """
    Schema for filtering history records.
    
    Attributes:
        operation_type (Optional[OperationType]): Filter by operation type
        start_date (Optional[datetime]): Start date for filtering
        end_date (Optional[datetime]): End date for filtering
        limit (int): Maximum number of records to return
    """
    operation_type: Optional[OperationType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000)


class HistoryDelete(BaseModel):
    """
    Schema for deleting history records.
    
    Attributes:
        ids (Optional[List[int]]): List of history IDs to delete
        delete_all (bool): Delete all user's history
    """
    ids: Optional[List[int]] = None
    delete_all: bool = False
    
    @field_validator('ids')
    @classmethod
    def validate_ids(cls, v: Optional[List[int]], info) -> Optional[List[int]]:
        """Validate that either ids or delete_all is provided."""
        values = info.data
        if v is None and not values.get('delete_all'):
            raise ValueError('Either provide ids or set delete_all to true')
        return v
