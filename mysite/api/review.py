from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Review
from mysite.database.schema import ReviewSchema, ReviewCreateSchema

review_router = APIRouter(prefix="/reviews", tags=["Reviews"])

@review_router.get("/", response_model=list[ReviewSchema])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@review_router.get("/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@review_router.put("/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

@review_router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}