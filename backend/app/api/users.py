from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.user_service import get_users, create_user, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.dependencies import require_admin
import uuid

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_admin)):
    return get_users(db, skip, limit)


@router.post("", response_model=UserOut, status_code=201)
def add_user(user_in: UserCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_user(db, user_in)


@router.put("/{user_id}", response_model=UserOut)
def edit_user(user_id: uuid.UUID, user_in: UserUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return update_user(db, user_id, user_in)


@router.delete("/{user_id}")
def remove_user(user_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_admin)):
    delete_user(db, user_id)
    return {"message": "User deleted"}
