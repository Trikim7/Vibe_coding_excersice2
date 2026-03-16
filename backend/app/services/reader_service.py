from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate
import uuid


def get_readers(db: Session, skip: int = 0, limit: int = 100) -> List[Reader]:
    return db.query(Reader).offset(skip).limit(limit).all()


def get_reader(db: Session, reader_id: uuid.UUID) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.id == reader_id).first()


def get_reader_by_ma(db: Session, ma_doc_gia: str) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.ma_doc_gia == ma_doc_gia).first()


def create_reader(db: Session, reader_in: ReaderCreate) -> Reader:
    existing = get_reader_by_ma(db, reader_in.ma_doc_gia)
    if existing:
        raise HTTPException(status_code=400, detail="Ma doc gia already exists")
    reader = Reader(**reader_in.model_dump())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


def update_reader(db: Session, reader_id: uuid.UUID, reader_in: ReaderUpdate) -> Reader:
    reader = get_reader(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    update_data = reader_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader


def delete_reader(db: Session, reader_id: uuid.UUID) -> bool:
    reader = get_reader(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(reader)
    db.commit()
    return True
