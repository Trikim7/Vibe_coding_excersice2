import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class Reader(Base):
    __tablename__ = "readers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_doc_gia = Column(String(20), unique=True, nullable=False, index=True)
    ho_ten = Column(String(100), nullable=False)
    lop = Column(String(50), nullable=True)
    ngay_sinh = Column(Date, nullable=True)
    gioi_tinh = Column(Enum("Nam", "Nu", name="gioi_tinh_enum"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
