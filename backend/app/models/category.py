import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_chuyen_nganh = Column(String(20), unique=True, nullable=False, index=True)
    ten = Column(String(100), nullable=False)
    mo_ta = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
