from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.borrow import Borrow
from app.models.book_copy import BookCopy
from app.models.book_title import BookTitle
from app.models.reader import Reader


def get_top_borrowed_books(db: Session, limit: int = 10) -> List[dict]:
    """Get top borrowed book titles."""
    results = (
        db.query(
            BookTitle.id,
            BookTitle.ma_dau_sach,
            BookTitle.ten,
            BookTitle.tac_gia,
            func.count(Borrow.id).label("borrow_count")
        )
        .join(BookCopy, BookCopy.dau_sach_id == BookTitle.id)
        .join(Borrow, Borrow.ma_sach == BookCopy.id)
        .group_by(BookTitle.id, BookTitle.ma_dau_sach, BookTitle.ten, BookTitle.tac_gia)
        .order_by(desc("borrow_count"))
        .limit(limit)
        .all()
    )
    return [
        {
            "id": str(r.id),
            "ma_dau_sach": r.ma_dau_sach,
            "ten": r.ten,
            "tac_gia": r.tac_gia,
            "borrow_count": r.borrow_count
        }
        for r in results
    ]


def get_unreturned_readers(db: Session) -> List[dict]:
    """Get readers with active (unreturned) borrows."""
    results = (
        db.query(
            Reader.id,
            Reader.ma_doc_gia,
            Reader.ho_ten,
            Reader.lop,
            Borrow.id.label("borrow_id"),
            Borrow.ngay_muon,
        )
        .join(Borrow, Borrow.ma_doc_gia == Reader.id)
        .filter(Borrow.tinh_trang.in_(["active", "overdue"]))
        .all()
    )
    return [
        {
            "reader_id": str(r.id),
            "ma_doc_gia": r.ma_doc_gia,
            "ho_ten": r.ho_ten,
            "lop": r.lop,
            "borrow_id": str(r.borrow_id),
            "ngay_muon": str(r.ngay_muon),
        }
        for r in results
    ]
