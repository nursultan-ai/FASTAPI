from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import get_db
from mysite.database.models import BlogPost
from mysite.database.schema import BlogPostInputSchema, BlogPostOutSchema

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/", response_model=List[BlogPostOutSchema])
def get_blog_posts(db: Session = Depends(get_db)):
    return db.query(BlogPost).all()


@router.get("/published", response_model=List[BlogPostOutSchema])
def get_published_posts(db: Session = Depends(get_db)):
    return db.query(BlogPost).filter(BlogPost.is_published == True).all()


@router.get("/slug/{slug}", response_model=BlogPostOutSchema)
def get_blog_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


@router.get("/{post_id}", response_model=BlogPostOutSchema)
def get_blog_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


@router.post("/", response_model=BlogPostOutSchema, status_code=status.HTTP_201_CREATED)
def create_blog_post(data: BlogPostInputSchema, db: Session = Depends(get_db)):
    existing = db.query(BlogPost).filter(BlogPost.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    post = BlogPost(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=BlogPostOutSchema)
def update_blog_post(post_id: int, data: BlogPostInputSchema, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    slug_conflict = db.query(BlogPost).filter(BlogPost.slug == data.slug, BlogPost.id != post_id).first()
    if slug_conflict:
        raise HTTPException(status_code=400, detail="Slug already exists")
    for key, value in data.model_dump().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    db.delete(post)
    db.commit()
