"""
Calculation history model.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class CalculationHistory(Base):
    """
    Calculation history model storing user's calculation records.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to users table
        operation_type (str): Type of operation (basic, advanced, conversion, finance)
        expression (str): Mathematical expression/input
        result (str): Calculation result
        created_at (datetime): Calculation timestamp
        user (relationship): Many-to-one relationship with User
    """
    
    __tablename__ = "calculation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    operation_type = Column(String(50), nullable=False)
    expression = Column(Text, nullable=False)
    result = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with user
    user = relationship("User", back_populates="calculations")
    
    def __repr__(self):
        return f"<CalculationHistory(id={self.id}, user_id={self.user_id}, operation='{self.operation_type}')>"