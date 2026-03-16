from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, date


class BookCopyBase(BaseModel):
    ma_ban_sao: str
    dau_sach_id: uuid.UUID
    tinh_trang: str = "available"
    ngay_nhap: Optional[date] = None


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(BaseModel):
    tinh_trang: Optional[str] = None
    ngay_nhap: Optional[date] = None


class BookCopyOut(BookCopyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
