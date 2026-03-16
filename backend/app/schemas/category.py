from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class CategoryBase(BaseModel):
    ma_chuyen_nganh: str
    ten: str
    mo_ta: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    ten: Optional[str] = None
    mo_ta: Optional[str] = None


class CategoryOut(CategoryBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
