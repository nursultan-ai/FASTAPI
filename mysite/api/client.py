from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import Client
from mysite.database.schema import ClientInputSchema, ClientOutSchema

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientOutSchema])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/featured", response_model=List[ClientOutSchema])
def get_featured_clients(db: Session = Depends(get_db)):
    return db.query(Client).filter(Client.is_featured == True).all()


@router.get("/{client_id}", response_model=ClientOutSchema)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientOutSchema, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientInputSchema, db: Session = Depends(get_db)):
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.put("/{client_id}", response_model=ClientOutSchema)
def update_client(client_id: int, data: ClientInputSchema, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in data.model_dump().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
