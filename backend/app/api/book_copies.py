from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.book_copy_service import get_book_copies, get_book_copy, create_book_copy, update_book_copy, delete_book_copy
from app.schemas.book_copy import BookCopyCreate, BookCopyUpdate, BookCopyOut
from app.core.dependencies import require_librarian_or_admin
import uuid

router = APIRouter(prefix="/api/book-copies", tags=["book-copies"])


@router.get("", response_model=List[BookCopyOut])
def list_book_copies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_book_copies(db, skip, limit)


@router.post("", response_model=BookCopyOut, status_code=201)
def add_book_copy(copy_in: BookCopyCreate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return create_book_copy(db, copy_in)


@router.get("/{copy_id}", response_model=BookCopyOut)
def get_one_copy(copy_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    c = get_book_copy(db, copy_id)
    if not c:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book copy not found")
    return c


@router.put("/{copy_id}", response_model=BookCopyOut)
def edit_book_copy(copy_id: uuid.UUID, copy_in: BookCopyUpdate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return update_book_copy(db, copy_id, copy_in)


@router.delete("/{copy_id}")
def remove_book_copy(copy_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    delete_book_copy(db, copy_id)
    return {"message": "Book copy deleted"}
