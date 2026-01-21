"""
Calculation history API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.schemas.history import HistoryResponse, HistoryFilter, HistoryDelete
from app.services.history_service import HistoryService
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.history_repository import HistoryRepository

router = APIRouter(prefix="/history", tags=["history"])
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


@router.get("/", response_model=List[HistoryResponse])
async def get_history(
    filters: HistoryFilter = Depends(),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> List[HistoryResponse]:
    """
    Get user's calculation history with optional filters.
    
    Args:
        filters (HistoryFilter): Filter criteria
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        List[HistoryResponse]: List of history records
    """
    try:
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        return history_service.get_user_history(user_id, filters)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}"
        )


@router.get("/stats")
async def get_history_stats(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get statistics about user's calculation history.
    
    Args:
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Statistics data
    """
    try:
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        return history_service.get_history_stats(user_id)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history stats: {str(e)}"
        )


@router.delete("/", response_model=Dict[str, Any])
async def delete_history(
    delete_data: HistoryDelete,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Delete history records.
    
    Args:
        delete_data (HistoryDelete): Delete configuration
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Dict[str, Any]: Deletion result
    """
    try:
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        return history_service.delete_history(user_id, delete_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete history: {str(e)}"
        )


@router.get("/export/csv")
async def export_history_csv(
    filters: HistoryFilter = Depends(),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Response:
    """
    Export user's history to CSV format.
    
    Args:
        filters (HistoryFilter): Filter criteria
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        Response: CSV file response
    """
    try:
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        csv_data = history_service.export_to_csv(user_id, filters)
        
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=calculation_history.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export history: {str(e)}"
        )


@router.get("/{history_id}", response_model=HistoryResponse)
async def get_history_by_id(
    history_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> HistoryResponse:
    """
    Get specific history record by ID.
    
    Args:
        history_id (int): History record ID
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        HistoryResponse: History record
        
    Raises:
        HTTPException: If record not found or access denied
    """
    try:
        history_repo = HistoryRepository(db)
        
        history = history_repo.get_history_by_id(history_id)
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="History record not found"
            )
        
        # Verify ownership
        if history.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this history record"
            )
        
        return HistoryResponse.from_orm(history)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history record: {str(e)}"
        )


@router.get("/export/csv")
async def export_csv(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Export user's calculation history as CSV file.
    
    Args:
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        CSV file download
    """
    try:
        import csv
        import io
        from datetime import datetime
        
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        # Get all user's history (pass empty filter for no filtering)
        empty_filter = HistoryFilter()
        history_records = history_service.get_user_history(user_id, empty_filter)
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['No', 'Expression', 'Result', 'Type', 'Date/Time'])
        
        # Write data
        for idx, record in enumerate(history_records, 1):
            writer.writerow([
                idx,
                record.expression,
                record.result,
                record.operation_type,
                record.created_at
            ])
        
        # Convert to bytes
        output.seek(0)
        csv_content = output.getvalue()
        
        # Return as file download
        filename = f"calculation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export CSV: {str(e)}"
        )


@router.get("/export/pdf")
async def export_pdf(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Export user's calculation history as PDF file.
    
    Args:
        user_id (int): Current user ID
        db (Session): Database session
        
    Returns:
        PDF file download
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from io import BytesIO
        from datetime import datetime
        
        history_repo = HistoryRepository(db)
        history_service = HistoryService(history_repo)
        
        # Get all user's history (pass empty filter for no filtering)
        empty_filter = HistoryFilter()
        history_records = history_service.get_user_history(user_id, empty_filter)
        
        # Create PDF in memory
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=20, bottomMargin=20)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4a6fa5'),
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        title = Paragraph("📊 Calculation History Report", title_style)
        elements.append(title)
        
        # Add generation info
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=12
        )
        info_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(info_text, info_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Create table data
        table_data = [['No', 'Expression', 'Result', 'Type', 'Date/Time']]
        
        for idx, record in enumerate(history_records, 1):
            table_data.append([
                str(idx),
                str(record.expression)[:40],  # Limit length
                str(record.result)[:20],
                record.operation_type,
                str(record.created_at)[:16]
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 2.2*inch, 1*inch, 1*inch, 1.3*inch])
        
        # Add style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a6fa5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ]))
        
        elements.append(table)
        
        # Add summary
        elements.append(Spacer(1, 0.3*inch))
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.grey
        )
        total = len(history_records)
        basic_count = sum(1 for r in history_records if r.operation_type == 'basic')
        advanced_count = sum(1 for r in history_records if r.operation_type == 'advanced')
        conversion_count = sum(1 for r in history_records if r.operation_type == 'conversion')
        finance_count = sum(1 for r in history_records if r.operation_type == 'finance')
        
        summary_text = (
            f"<b>Summary:</b> Total Calculations: {total} | "
            f"Basic: {basic_count} | Advanced: {advanced_count} | "
            f"Conversion: {conversion_count} | Finance: {finance_count}"
        )
        elements.append(Paragraph(summary_text, summary_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF content
        pdf_buffer.seek(0)
        
        # Return as file download
        filename = f"calculation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF: {str(e)}"
        )