from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import ContactRequest
from mysite.database.schema import ContactRequestInputSchema, ContactRequestOutSchema

router = APIRouter(prefix="/contacts", tags=["Contact Requests"])


@router.get("/", response_model=List[ContactRequestOutSchema])
def get_contact_requests(db: Session = Depends(get_db)):
    return db.query(ContactRequest).all()


@router.get("/{contact_id}", response_model=ContactRequestOutSchema)
def get_contact_request(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactRequest).filter(ContactRequest.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact request not found")
    return contact


@router.post("/", response_model=ContactRequestOutSchema, status_code=status.HTTP_201_CREATED)
def create_contact_request(data: ContactRequestInputSchema, db: Session = Depends(get_db)):
    contact = ContactRequest(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.put("/{contact_id}", response_model=ContactRequestOutSchema)
def update_contact_request(contact_id: int, data: ContactRequestInputSchema, db: Session = Depends(get_db)):
    contact = db.query(ContactRequest).filter(ContactRequest.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact request not found")
    for key, value in data.model_dump().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_request(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactRequest).filter(ContactRequest.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact request not found")
    db.delete(contact)
    db.commit()
