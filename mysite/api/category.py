from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Category
from mysite.database.schema import CategorySchema, CategoryCreateSchema

category_router = APIRouter(prefix="/categories", tags=["Categories"])

@category_router.get("/", response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@category_router.post("/", response_model=CategorySchema)
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    db_cat = Category(**category.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@category_router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@category_router.put("/{category_id}", response_model=CategorySchema)
def update_category(category_id: int, category: CategoryCreateSchema, db: Session = Depends(get_db)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db_cat.category_name = category.category_name
    db.commit()
    db.refresh(db_cat)
    return db_cat

@category_router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(Category).filter(Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_cat)
    db.commit()
    return {"message": "Category deleted successfully"}