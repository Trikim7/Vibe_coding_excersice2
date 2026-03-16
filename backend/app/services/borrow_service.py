from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.borrow import Borrow
from app.models.book_copy import BookCopy
from app.models.reader import Reader
from app.schemas.borrow import BorrowCreate
import uuid

BORROW_DURATION_DAYS = 14


def get_borrows(db: Session, skip: int = 0, limit: int = 100) -> List[Borrow]:
    return db.query(Borrow).offset(skip).limit(limit).all()


def get_borrow(db: Session, borrow_id: uuid.UUID) -> Optional[Borrow]:
    return db.query(Borrow).filter(Borrow.id == borrow_id).first()


def create_borrow(db: Session, borrow_in: BorrowCreate, librarian_id: uuid.UUID) -> Borrow:
    # Check reader exists
    reader = db.query(Reader).filter(Reader.id == borrow_in.ma_doc_gia).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    # Check reader has no active borrow
    active_borrow = db.query(Borrow).filter(
        Borrow.ma_doc_gia == borrow_in.ma_doc_gia,
        Borrow.tinh_trang == "active"
    ).first()
    if active_borrow:
        raise HTTPException(status_code=400, detail="Reader already has an active borrow")

    # Check book copy exists and is available
    copy = db.query(BookCopy).filter(BookCopy.id == borrow_in.ma_sach).first()
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    if copy.tinh_trang != "available":
        raise HTTPException(status_code=400, detail=f"Book copy is not available (status: {copy.tinh_trang})")

    # Create borrow record
    today = date.today()
    borrow = Borrow(
        ma_sach=borrow_in.ma_sach,
        ma_doc_gia=borrow_in.ma_doc_gia,
        ma_thu_thu=librarian_id,
        ngay_muon=today,
        tinh_trang="active",
    )
    copy.tinh_trang = "borrowed"

    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def return_borrow(db: Session, borrow_id: uuid.UUID) -> Borrow:
    borrow = get_borrow(db, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.tinh_trang != "active":
        raise HTTPException(status_code=400, detail="Borrow is not active")

    today = date.today()
    borrow.ngay_tra = today
    borrow.tinh_trang = "returned"

    # Update book copy status
    copy = db.query(BookCopy).filter(BookCopy.id == borrow.ma_sach).first()
    if copy:
        copy.tinh_trang = "available"

    db.commit()
    db.refresh(borrow)
    return borrow


def update_overdue_borrows(db: Session):
    """Mark borrows as overdue if past due date (14 days)."""
    today = date.today()
    active_borrows = db.query(Borrow).filter(Borrow.tinh_trang == "active").all()
    for borrow in active_borrows:
        due_date = borrow.ngay_muon + timedelta(days=BORROW_DURATION_DAYS)
        if today > due_date:
            borrow.tinh_trang = "overdue"
    db.commit()
