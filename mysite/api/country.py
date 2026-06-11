from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import Country
from mysite.database.schema import CountryInputSchema, CountryOutSchema

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=List[CountryOutSchema])
def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()


@router.get("/{country_id}", response_model=CountryOutSchema)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.post("/", response_model=CountryOutSchema, status_code=status.HTTP_201_CREATED)
def create_country(data: CountryInputSchema, db: Session = Depends(get_db)):
    country = Country(**data.model_dump())
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


@router.put("/{country_id}", response_model=CountryOutSchema)
def update_country(country_id: int, data: CountryInputSchema, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in data.model_dump().items():
        setattr(country, key, value)
    db.commit()
    db.refresh(country)
    return country


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(country)
    db.commit()
