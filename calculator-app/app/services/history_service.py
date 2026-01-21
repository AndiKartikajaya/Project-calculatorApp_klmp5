"""
Service layer for calculation history operations.
"""

from typing import List, Optional
import logging
from datetime import datetime
import csv
import io

from app.repositories.history_repository import HistoryRepository
from app.schemas.history import HistoryResponse, HistoryFilter, HistoryDelete

logger = logging.getLogger(__name__)


class HistoryService:
    """
    Service class for calculation history operations.
    
    Methods:
        add_to_history: Add calculation to history
        get_user_history: Get user's calculation history
        delete_history: Delete history records
        export_to_csv: Export history to CSV format
        get_history_stats: Get statistics about user's history
    """
    
    def __init__(self, history_repository: HistoryRepository):
        """
        Initialize HistoryService.
        
        Args:
            history_repository (HistoryRepository): History repository instance
        """
        self.history_repository = history_repository
    
    def add_to_history(self, user_id: int, operation_type: str, 
                      expression: str, result: str) -> HistoryResponse:
        """
        Add calculation to user's history.
        
        Args:
            user_id (int): User ID
            operation_type (str): Type of operation
            expression (str): Mathematical expression
            result (str): Calculation result
            
        Returns:
            HistoryResponse: Created history record
        """
        try:
            history = self.history_repository.create_history(
                user_id=user_id,
                operation_type=operation_type,
                expression=expression,
                result=str(result)
            )
            
            return HistoryResponse.from_orm(history)
            
        except Exception as e:
            logger.error(f"Error adding to history for user {user_id}: {str(e)}")
            raise
    
    def get_user_history(self, user_id: int, filters: HistoryFilter) -> List[HistoryResponse]:
        """
        Get user's calculation history with filters.
        
        Args:
            user_id (int): User ID
            filters (HistoryFilter): Filter criteria
            
        Returns:
            List[HistoryResponse]: List of history records
        """
        try:
            history_records = self.history_repository.get_user_history(user_id, filters)
            
            return [
                HistoryResponse.from_orm(record) 
                for record in history_records
            ]
            
        except Exception as e:
            logger.error(f"Error getting history for user {user_id}: {str(e)}")
            raise
    
    def delete_history(self, user_id: int, delete_data: HistoryDelete) -> dict:
        """
        Delete history records.
        
        Args:
            user_id (int): User ID
            delete_data (HistoryDelete): Delete configuration
            
        Returns:
            dict: Result of deletion
        """
        try:
            if delete_data.delete_all:
                count = self.history_repository.delete_user_history(user_id)
                message = f"All {count} history records deleted"
            elif delete_data.ids:
                count = self.history_repository.delete_user_history(user_id, delete_data.ids)
                message = f"{count} history records deleted"
            else:
                return {"message": "No action taken", "count": 0}
            
            return {"message": message, "count": count}
            
        except Exception as e:
            logger.error(f"Error deleting history for user {user_id}: {str(e)}")
            raise
    
    def export_to_csv(self, user_id: int, filters: HistoryFilter) -> str:
        """
        Export user's history to CSV format.
        
        Args:
            user_id (int): User ID
            filters (HistoryFilter): Filter criteria
            
        Returns:
            str: CSV data as string
        """
        try:
            history_records = self.get_user_history(user_id, filters)
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["ID", "Operation Type", "Expression", "Result", "Timestamp"])
            
            # Write data
            for record in history_records:
                writer.writerow([
                    record.id,
                    record.operation_type,
                    record.expression,
                    record.result,
                    record.created_at.isoformat()
                ])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting history for user {user_id}: {str(e)}")
            raise
    
    def get_history_stats(self, user_id: int) -> dict:
        """
        Get statistics about user's calculation history.
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Statistics dictionary
        """
        try:
            total_count = self.history_repository.get_user_history_count(user_id)
            
            # Get recent history for operation type analysis
            recent_filters = HistoryFilter(limit=1000)
            recent_history = self.history_repository.get_user_history(user_id, recent_filters)
            
            # Count by operation type
            operation_counts = {}
            for record in recent_history:
                op_type = record.operation_type
                operation_counts[op_type] = operation_counts.get(op_type, 0) + 1
            
            return {
                "total_calculations": total_count,
                "operation_counts": operation_counts,
                "recent_activity_count": len(recent_history)
            }
            
        except Exception as e:
            logger.error(f"Error getting stats for user {user_id}: {str(e)}")
            raise