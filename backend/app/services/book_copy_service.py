from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.book_copy import BookCopy
from app.schemas.book_copy import BookCopyCreate, BookCopyUpdate
import uuid


def get_book_copies(db: Session, skip: int = 0, limit: int = 100) -> List[BookCopy]:
    return db.query(BookCopy).offset(skip).limit(limit).all()


def get_book_copy(db: Session, copy_id: uuid.UUID) -> Optional[BookCopy]:
    return db.query(BookCopy).filter(BookCopy.id == copy_id).first()


def create_book_copy(db: Session, copy_in: BookCopyCreate) -> BookCopy:
    existing = db.query(BookCopy).filter(BookCopy.ma_ban_sao == copy_in.ma_ban_sao).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma ban sao already exists")
    copy = BookCopy(**copy_in.model_dump())
    db.add(copy)
    db.commit()
    db.refresh(copy)
    return copy


def update_book_copy(db: Session, copy_id: uuid.UUID, copy_in: BookCopyUpdate) -> BookCopy:
    copy = get_book_copy(db, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    update_data = copy_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(copy, key, value)
    db.commit()
    db.refresh(copy)
    return copy


def delete_book_copy(db: Session, copy_id: uuid.UUID) -> bool:
    copy = get_book_copy(db, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    db.delete(copy)
    db.commit()
    return True
