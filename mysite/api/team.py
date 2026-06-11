from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import TeamMember
from mysite.database.schema import TeamMemberInputSchema, TeamMemberOutSchema

router = APIRouter(prefix="/team", tags=["Team"])


@router.get("/", response_model=List[TeamMemberOutSchema])
def get_team_members(db: Session = Depends(get_db)):
    return db.query(TeamMember).all()


@router.get("/active", response_model=List[TeamMemberOutSchema])
def get_active_team_members(db: Session = Depends(get_db)):
    return db.query(TeamMember).filter(TeamMember.is_active == True).all()


@router.get("/{member_id}", response_model=TeamMemberOutSchema)
def get_team_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return member


@router.post("/", response_model=TeamMemberOutSchema, status_code=status.HTTP_201_CREATED)
def create_team_member(data: TeamMemberInputSchema, db: Session = Depends(get_db)):
    member = TeamMember(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.put("/{member_id}", response_model=TeamMemberOutSchema)
def update_team_member(member_id: int, data: TeamMemberInputSchema, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    for key, value in data.model_dump().items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    db.delete(member)
    db.commit()
