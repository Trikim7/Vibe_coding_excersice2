from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.report_service import get_top_borrowed_books, get_unreturned_readers
from app.core.dependencies import require_librarian_or_admin

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/top-borrowed")
def top_borrowed(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_top_borrowed_books(db, limit)


@router.get("/unreturned-readers")
def unreturned_readers(db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_unreturned_readers(db)
