from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=List[ReviewOutSchema])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.get("/published", response_model=List[ReviewOutSchema])
def get_published_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.is_published == True).all()


@router.get("/{review_id}", response_model=ReviewOutSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/", response_model=ReviewOutSchema, status_code=status.HTTP_201_CREATED)
def create_review(data: ReviewInputSchema, db: Session = Depends(get_db)):
    if not 1 <= data.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    review = Review(**data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.put("/{review_id}", response_model=ReviewOutSchema)
def update_review(review_id: int, data: ReviewInputSchema, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if not 1 <= data.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    for key, value in data.model_dump().items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
