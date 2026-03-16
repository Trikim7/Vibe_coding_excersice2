from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.reader_service import get_readers, get_reader, create_reader, update_reader, delete_reader
from app.schemas.reader import ReaderCreate, ReaderUpdate, ReaderOut
from app.core.dependencies import require_librarian_or_admin
import uuid

router = APIRouter(prefix="/api/readers", tags=["readers"])


@router.get("", response_model=List[ReaderOut])
def list_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_readers(db, skip, limit)


@router.post("", response_model=ReaderOut, status_code=201)
def add_reader(reader_in: ReaderCreate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return create_reader(db, reader_in)


@router.get("/{reader_id}", response_model=ReaderOut)
def get_one_reader(reader_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    reader = get_reader(db, reader_id)
    if not reader:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.put("/{reader_id}", response_model=ReaderOut)
def edit_reader(reader_id: uuid.UUID, reader_in: ReaderUpdate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return update_reader(db, reader_id, reader_in)


@router.delete("/{reader_id}")
def remove_reader(reader_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    delete_reader(db, reader_id)
    return {"message": "Reader deleted"}
