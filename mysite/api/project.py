from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import Project, ProjectImage
from mysite.database.schema import (
    ProjectInputSchema, ProjectOutSchema,
    ProjectImageInputSchema, ProjectImageOutSchema,
)

router = APIRouter(prefix="/projects", tags=["Projects"])
image_router = APIRouter(prefix="/project-images", tags=["Project Images"])


# ── Projects ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ProjectOutSchema])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@router.get("/featured", response_model=List[ProjectOutSchema])
def get_featured_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.is_featured == True).all()


@router.get("/{project_id}", response_model=ProjectOutSchema)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectOutSchema, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectInputSchema, db: Session = Depends(get_db)):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectOutSchema)
def update_project(project_id: int, data: ProjectInputSchema, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in data.model_dump().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


# ── Project Images ────────────────────────────────────────────────────────────

@image_router.get("/", response_model=List[ProjectImageOutSchema])
def get_project_images(db: Session = Depends(get_db)):
    return db.query(ProjectImage).all()


@image_router.get("/{image_id}", response_model=ProjectImageOutSchema)
def get_project_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Project image not found")
    return image


@image_router.post("/", response_model=ProjectImageOutSchema, status_code=status.HTTP_201_CREATED)
def create_project_image(data: ProjectImageInputSchema, db: Session = Depends(get_db)):
    image = ProjectImage(**data.model_dump())
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@image_router.put("/{image_id}", response_model=ProjectImageOutSchema)
def update_project_image(image_id: int, data: ProjectImageInputSchema, db: Session = Depends(get_db)):
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Project image not found")
    for key, value in data.model_dump().items():
        setattr(image, key, value)
    db.commit()
    db.refresh(image)
    return image


@image_router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Project image not found")
    db.delete(image)
    db.commit()
