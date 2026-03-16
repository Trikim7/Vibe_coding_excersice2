import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


class BookTitle(Base):
    __tablename__ = "book_titles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_dau_sach = Column(String(20), unique=True, nullable=False, index=True)
    ten = Column(String(200), nullable=False)
    nha_xuat_ban = Column(String(100), nullable=True)
    so_trang = Column(Integer, nullable=True)
    kich_thuoc = Column(String(50), nullable=True)
    tac_gia = Column(String(100), nullable=True)
    so_luong = Column(Integer, default=0)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", backref="book_titles")
    copies = relationship("BookCopy", backref="book_title")
