from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.category_service import get_categories, get_category, create_category, update_category, delete_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.core.dependencies import require_librarian_or_admin
import uuid

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[CategoryOut])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return get_categories(db, skip, limit)


@router.post("", response_model=CategoryOut, status_code=201)
def add_category(cat_in: CategoryCreate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return create_category(db, cat_in)


@router.get("/{category_id}", response_model=CategoryOut)
def get_one_category(category_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    cat = get_category(db, category_id)
    if not cat:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.put("/{category_id}", response_model=CategoryOut)
def edit_category(category_id: uuid.UUID, cat_in: CategoryUpdate, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    return update_category(db, category_id, cat_in)


@router.delete("/{category_id}")
def remove_category(category_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_librarian_or_admin)):
    delete_category(db, category_id)
    return {"message": "Category deleted"}
