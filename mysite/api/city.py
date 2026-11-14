from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import City
from mysite.database.schema import CitySchema, CityCreateSchema

city_router = APIRouter(prefix="/cities", tags=["Cities"])

@city_router.get("/", response_model=list[CitySchema])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.post("/", response_model=CitySchema)
def create_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@city_router.get("/{city_id}", response_model=CitySchema)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@city_router.put("/{city_id}", response_model=CitySchema)
def update_city(city_id: int, city: CityCreateSchema, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db_city.city_name = city.city_name
    db.commit()
    db.refresh(db_city)
    return db_city

@city_router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return {"message": "City deleted successfully"}