from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.book_title import BookTitle
from app.models.book_copy import BookCopy
from app.schemas.book_title import BookTitleCreate, BookTitleUpdate
import uuid


def get_book_titles(db: Session, skip: int = 0, limit: int = 100) -> List[BookTitle]:
    return db.query(BookTitle).offset(skip).limit(limit).all()


def get_book_title(db: Session, title_id: uuid.UUID) -> Optional[BookTitle]:
    return db.query(BookTitle).filter(BookTitle.id == title_id).first()


def create_book_title(db: Session, title_in: BookTitleCreate) -> BookTitle:
    existing = db.query(BookTitle).filter(BookTitle.ma_dau_sach == title_in.ma_dau_sach).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma dau sach already exists")
    title = BookTitle(**title_in.model_dump())
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


def update_book_title(db: Session, title_id: uuid.UUID, title_in: BookTitleUpdate) -> BookTitle:
    title = get_book_title(db, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Book title not found")
    update_data = title_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(title, key, value)
    db.commit()
    db.refresh(title)
    return title


def delete_book_title(db: Session, title_id: uuid.UUID) -> bool:
    title = get_book_title(db, title_id)
    if not title:
        raise HTTPException(status_code=404, detail="Book title not found")
    db.delete(title)
    db.commit()
    return True


def get_copies_for_title(db: Session, title_id: uuid.UUID) -> List[BookCopy]:
    return db.query(BookCopy).filter(BookCopy.dau_sach_id == title_id).all()
