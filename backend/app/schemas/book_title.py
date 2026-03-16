from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class BookTitleBase(BaseModel):
    ma_dau_sach: str
    ten: str
    nha_xuat_ban: Optional[str] = None
    so_trang: Optional[int] = None
    kich_thuoc: Optional[str] = None
    tac_gia: Optional[str] = None
    so_luong: int = 0
    category_id: Optional[uuid.UUID] = None


class BookTitleCreate(BookTitleBase):
    pass


class BookTitleUpdate(BaseModel):
    ten: Optional[str] = None
    nha_xuat_ban: Optional[str] = None
    so_trang: Optional[int] = None
    kich_thuoc: Optional[str] = None
    tac_gia: Optional[str] = None
    so_luong: Optional[int] = None
    category_id: Optional[uuid.UUID] = None


class BookTitleOut(BookTitleBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
