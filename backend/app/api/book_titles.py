from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.book_title_service import (
    get_book_titles, get_book_title, create_book_title, update_book_title, delete_book_title, get_copies_for_title
)
from app.schemas.book_title import BookTitleCreate, BookTitleUpdate, BookTitleOut
from app.schemas.book_copy import BookCopyOut
from app.core.dependencies import require_librarian_or_admin
import uuid

router = APIRouter(prefix="/api/book-titles", tags=["book-titles"])


@router.get("", response_model=List[BookTitleOut])
def list_book_titles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_book_titles(db, skip, limit)


@router.post("", response_model=BookTitleOut, status_code=201)
def add_book_title(title_in: BookTitleCreate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return create_book_title(db, title_in)


@router.get("/{title_id}", response_model=BookTitleOut)
def get_one_title(title_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    t = get_book_title(db, title_id)
    if not t:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book title not found")
    return t


@router.put("/{title_id}", response_model=BookTitleOut)
def edit_book_title(title_id: uuid.UUID, title_in: BookTitleUpdate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return update_book_title(db, title_id, title_in)


@router.delete("/{title_id}")
def remove_book_title(title_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    delete_book_title(db, title_id)
    return {"message": "Book title deleted"}


@router.get("/{title_id}/copies", response_model=List[BookCopyOut])
def list_copies_for_title(title_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_copies_for_title(db, title_id)
