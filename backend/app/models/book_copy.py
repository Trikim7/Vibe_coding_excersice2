import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_ban_sao = Column(String(20), unique=True, nullable=False, index=True)
    dau_sach_id = Column(UUID(as_uuid=True), ForeignKey("book_titles.id"), nullable=False)
    tinh_trang = Column(
        Enum("available", "borrowed", "lost", "repair", name="copy_status"),
        nullable=False,
        default="available"
    )
    ngay_nhap = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
