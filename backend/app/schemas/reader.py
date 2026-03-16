from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, date


class ReaderBase(BaseModel):
    ma_doc_gia: str
    ho_ten: str
    lop: Optional[str] = None
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    ho_ten: Optional[str] = None
    lop: Optional[str] = None
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None


class ReaderOut(ReaderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
