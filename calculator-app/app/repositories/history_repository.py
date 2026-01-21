"""
Repository layer for calculation history database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime
import logging

from app.models.calculation import CalculationHistory
from app.schemas.history import HistoryFilter
from app.schemas.calculator import OperationType

logger = logging.getLogger(__name__)


class HistoryRepository:
    """
    Repository class for calculation history database operations.
    
    Methods:
        create_history: Create new history record
        get_history_by_id: Get history record by ID
        get_user_history: Get user's calculation history
        delete_history: Delete history record(s)
        get_user_history_count: Count user's history records
    """
    
    def __init__(self, db: Session):
        """
        Initialize HistoryRepository.
        
        Args:
            db (Session): Database session
        """
        self.db = db
    
    def create_history(self, user_id: int, operation_type: OperationType, 
                      expression: str, result: str) -> CalculationHistory:
        """
        Create a new calculation history record.
        
        Args:
            user_id (int): User ID
            operation_type (OperationType): Type of operation
            expression (str): Mathematical expression
            result (str): Calculation result
            
        Returns:
            CalculationHistory: Created history record
        """
        try:
            history = CalculationHistory(
                user_id=user_id,
                operation_type=operation_type,
                expression=expression,
                result=result
            )
            self.db.add(history)
            self.db.commit()
            self.db.refresh(history)
            logger.debug(f"History created for user {user_id}: {operation_type}")
            return history
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating history for user {user_id}: {str(e)}")
            raise
    
    def get_history_by_id(self, history_id: int) -> Optional[CalculationHistory]:
        """
        Get history record by ID.
        
        Args:
            history_id (int): History record ID
            
        Returns:
            Optional[CalculationHistory]: History record or None
        """
        return self.db.query(CalculationHistory).filter(
            CalculationHistory.id == history_id
        ).first()
    
    def get_user_history(self, user_id: int, filters: HistoryFilter) -> List[CalculationHistory]:
        """
        Get user's calculation history with optional filters.
        
        Args:
            user_id (int): User ID
            filters (HistoryFilter): Filter criteria
            
        Returns:
            List[CalculationHistory]: List of history records
        """
        query = self.db.query(CalculationHistory).filter(
            CalculationHistory.user_id == user_id
        )
        
        # Apply filters
        if filters.operation_type:
            query = query.filter(
                CalculationHistory.operation_type == filters.operation_type
            )
        
        if filters.start_date:
            query = query.filter(
                CalculationHistory.created_at >= filters.start_date
            )
        
        if filters.end_date:
            query = query.filter(
                CalculationHistory.created_at <= filters.end_date
            )
        
        # Order by latest first and apply limit
        query = query.order_by(desc(CalculationHistory.created_at))
        
        if filters.limit:
            query = query.limit(filters.limit)
        
        return query.all()
    
    def delete_history(self, history_id: int, user_id: Optional[int] = None) -> bool:
        """
        Delete a history record.
        
        Args:
            history_id (int): History record ID
            user_id (Optional[int]): Optional user ID for verification
            
        Returns:
            bool: True if deleted, False if not found
        """
        try:
            query = self.db.query(CalculationHistory).filter(
                CalculationHistory.id == history_id
            )
            
            if user_id:
                query = query.filter(CalculationHistory.user_id == user_id)
            
            history = query.first()
            
            if not history:
                return False
            
            self.db.delete(history)
            self.db.commit()
            logger.info(f"History deleted: {history_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting history {history_id}: {str(e)}")
            raise
    
    def delete_user_history(self, user_id: int, history_ids: Optional[List[int]] = None) -> int:
        """
        Delete user's history records.
        
        Args:
            user_id (int): User ID
            history_ids (Optional[List[int]]): List of history IDs to delete
            
        Returns:
            int: Number of records deleted
        """
        try:
            query = self.db.query(CalculationHistory).filter(
                CalculationHistory.user_id == user_id
            )
            
            if history_ids:
                query = query.filter(CalculationHistory.id.in_(history_ids))
            
            count = query.count()
            query.delete(synchronize_session=False)
            self.db.commit()
            
            logger.info(f"Deleted {count} history records for user {user_id}")
            return count
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting history for user {user_id}: {str(e)}")
            raise
    
    def get_user_history_count(self, user_id: int) -> int:
        """
        Get count of user's history records.
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Number of history records
        """
        return self.db.query(CalculationHistory).filter(
            CalculationHistory.user_id == user_id
        ).count()