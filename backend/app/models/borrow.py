import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_sach = Column(UUID(as_uuid=True), ForeignKey("book_copies.id"), nullable=False)
    ma_doc_gia = Column(UUID(as_uuid=True), ForeignKey("readers.id"), nullable=False)
    ma_thu_thu = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ngay_muon = Column(Date, nullable=False)
    ngay_tra = Column(Date, nullable=True)
    tinh_trang = Column(
        Enum("active", "returned", "overdue", name="borrow_status"),
        nullable=False,
        default="active"
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    book_copy = relationship("BookCopy", backref="borrows")
    reader = relationship("Reader", backref="borrows")
    librarian = relationship("User", backref="borrows")
