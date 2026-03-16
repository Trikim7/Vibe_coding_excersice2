from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, date


class BorrowCreate(BaseModel):
    ma_sach: uuid.UUID
    ma_doc_gia: uuid.UUID


class BorrowOut(BaseModel):
    id: uuid.UUID
    ma_sach: uuid.UUID
    ma_doc_gia: uuid.UUID
    ma_thu_thu: uuid.UUID
    ngay_muon: date
    ngay_tra: Optional[date] = None
    tinh_trang: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BorrowReturn(BaseModel):
    pass
