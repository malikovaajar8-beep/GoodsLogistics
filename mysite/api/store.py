from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Store
from mysite.database.schema import StoreSchema, StoreCreateSchema

store_router = APIRouter(prefix="/stores", tags=["Stores"])

@store_router.get("/", response_model=list[StoreSchema])
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()

@store_router.post("/", response_model=StoreSchema)
def create_store(store: StoreCreateSchema, db: Session = Depends(get_db)):
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

@store_router.get("/{store_id}", response_model=StoreSchema)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@store_router.put("/{store_id}", response_model=StoreSchema)
def update_store(store_id: int, store: StoreCreateSchema, db: Session = Depends(get_db)):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    for key, value in store.dict().items():
        setattr(db_store, key, value)
    db.commit()
    db.refresh(db_store)
    return db_store

@store_router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(db_store)
    db.commit()
    return {"message": "Store deleted successfully"}