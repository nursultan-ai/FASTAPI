from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from mysite.database.models import RoleChoices, ProjectStatusChoices, ContactStatusChoices


# ── Auth ──────────────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    user_role: RoleChoices = RoleChoices.client


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ── Country ───────────────────────────────────────────────────────────────────
class CountryInputSchema(BaseModel):
    country_name: str
    country_code: Optional[str] = None


class CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_code: Optional[str] = None

    class Config:
        from_attributes = True


# ── UserProfile ───────────────────────────────────────────────────────────────
class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    user_image: Optional[str] = None
    user_role: RoleChoices = RoleChoices.client


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: Optional[str] = None
    user_image: Optional[str] = None
    user_role: RoleChoices
    registered_date: datetime

    class Config:
        from_attributes = True


# ── ServiceCategory ───────────────────────────────────────────────────────────
class ServiceCategoryInputSchema(BaseModel):
    name: str
    icon: Optional[str] = None


class ServiceCategoryOutSchema(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None

    class Config:
        from_attributes = True


# ── Service ───────────────────────────────────────────────────────────────────
class ServiceInputSchema(BaseModel):
    title: str
    description: str
    icon: Optional[str] = None
    price: Optional[int] = None
    is_featured: bool = False
    category_id: int


class ServiceOutSchema(BaseModel):
    id: int
    title: str
    description: str
    icon: Optional[str] = None
    price: Optional[int] = None
    is_featured: bool
    category_id: int
    category: Optional[ServiceCategoryOutSchema] = None

    class Config:
        from_attributes = True


# ── TeamMember ────────────────────────────────────────────────────────────────
class TeamMemberInputSchema(BaseModel):
    first_name: str
    last_name: str
    position: str
    bio: Optional[str] = None
    photo: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    country_id: Optional[int] = None
    is_active: bool = True


class TeamMemberOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    bio: Optional[str] = None
    photo: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    country_id: Optional[int] = None
    is_active: bool
    country: Optional[CountryOutSchema] = None

    class Config:
        from_attributes = True


# ── Client ────────────────────────────────────────────────────────────────────
class ClientInputSchema(BaseModel):
    company_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    country_id: Optional[int] = None
    is_featured: bool = False


class ClientOutSchema(BaseModel):
    id: int
    company_name: str
    logo: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    country_id: Optional[int] = None
    is_featured: bool
    country: Optional[CountryOutSchema] = None

    class Config:
        from_attributes = True


# ── ProjectImage ──────────────────────────────────────────────────────────────
class ProjectImageInputSchema(BaseModel):
    project_id: int
    image_url: str
    caption: Optional[str] = None


class ProjectImageOutSchema(BaseModel):
    id: int
    project_id: int
    image_url: str
    caption: Optional[str] = None

    class Config:
        from_attributes = True


# ── Project ───────────────────────────────────────────────────────────────────
class ProjectInputSchema(BaseModel):
    title: str
    description: str
    cover_image: Optional[str] = None
    project_url: Optional[str] = None
    service_id: int
    client_id: Optional[int] = None
    status: ProjectStatusChoices = ProjectStatusChoices.in_progress
    is_featured: bool = False
    completed_date: Optional[datetime] = None


class ProjectOutSchema(BaseModel):
    id: int
    title: str
    description: str
    cover_image: Optional[str] = None
    project_url: Optional[str] = None
    service_id: int
    client_id: Optional[int] = None
    status: ProjectStatusChoices
    is_featured: bool
    created_date: datetime
    completed_date: Optional[datetime] = None
    images: List[ProjectImageOutSchema] = []

    class Config:
        from_attributes = True


# ── Review ────────────────────────────────────────────────────────────────────
class ReviewInputSchema(BaseModel):
    client_id: int
    author_name: str
    author_position: Optional[str] = None
    author_photo: Optional[str] = None
    rating: int
    text: str
    is_published: bool = False


class ReviewOutSchema(BaseModel):
    id: int
    client_id: int
    author_name: str
    author_position: Optional[str] = None
    author_photo: Optional[str] = None
    rating: int
    text: str
    is_published: bool
    created_date: datetime

    class Config:
        from_attributes = True


# ── ContactRequest ────────────────────────────────────────────────────────────
class ContactRequestInputSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    user_id: Optional[int] = None


class ContactRequestOutSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str
    status: ContactStatusChoices
    user_id: Optional[int] = None
    created_date: datetime

    class Config:
        from_attributes = True


# ── BlogPost ──────────────────────────────────────────────────────────────────
class BlogPostInputSchema(BaseModel):
    title: str
    slug: str
    preview_text: str
    content: str
    cover_image: Optional[str] = None
    is_published: bool = False


class BlogPostOutSchema(BaseModel):
    id: int
    title: str
    slug: str
    preview_text: str
    content: str
    cover_image: Optional[str] = None
    is_published: bool
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True