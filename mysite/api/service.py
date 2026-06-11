from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import Service, ServiceCategory
from mysite.database.schema import (
    ServiceInputSchema, ServiceOutSchema,
    ServiceCategoryInputSchema, ServiceCategoryOutSchema,
)

router = APIRouter(prefix="/services", tags=["Services"])
category_router = APIRouter(prefix="/service-categories", tags=["Service Categories"])


# ── Service Categories ────────────────────────────────────────────────────────

@category_router.get("/", response_model=List[ServiceCategoryOutSchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).all()


@category_router.get("/{category_id}", response_model=ServiceCategoryOutSchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.post("/", response_model=ServiceCategoryOutSchema, status_code=status.HTTP_201_CREATED)
def create_category(data: ServiceCategoryInputSchema, db: Session = Depends(get_db)):
    category = ServiceCategory(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@category_router.put("/{category_id}", response_model=ServiceCategoryOutSchema)
def update_category(category_id: int, data: ServiceCategoryInputSchema, db: Session = Depends(get_db)):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in data.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()


# ── Services ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ServiceOutSchema])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/featured", response_model=List[ServiceOutSchema])
def get_featured_services(db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.is_featured == True).all()


@router.get("/{service_id}", response_model=ServiceOutSchema)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.post("/", response_model=ServiceOutSchema, status_code=status.HTTP_201_CREATED)
def create_service(data: ServiceInputSchema, db: Session = Depends(get_db)):
    service = Service(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/{service_id}", response_model=ServiceOutSchema)
def update_service(service_id: int, data: ServiceInputSchema, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in data.model_dump().items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
