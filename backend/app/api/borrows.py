from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.borrow_service import get_borrows, create_borrow, return_borrow
from app.schemas.borrow import BorrowCreate, BorrowOut
from app.core.dependencies import require_librarian_or_admin, get_current_user
from app.models.user import User
import uuid

router = APIRouter(prefix="/api/borrows", tags=["borrows"])


@router.get("", response_model=List[BorrowOut])
def list_borrows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_borrows(db, skip, limit)


@router.post("", response_model=BorrowOut, status_code=201)
def add_borrow(
    borrow_in: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian_or_admin)
):
    return create_borrow(db, borrow_in, current_user.id)


@router.post("/{borrow_id}/return", response_model=BorrowOut)
def do_return(borrow_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return return_borrow(db, borrow_id)
