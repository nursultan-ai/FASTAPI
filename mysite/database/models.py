from mysite.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Text, Boolean
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    admin = 'admin'


class ProjectStatusChoices(str, PyEnum):
    in_progress = 'В работе'
    completed = 'Завершён'
    on_hold = 'На паузе'


class ContactStatusChoices(str, PyEnum):
    new = 'Новый'
    in_review = 'В обработке'
    closed = 'Закрыт'


# ── Страны ───────────────────────────────────────────────────────────────────
class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(100), unique=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    team_members: Mapped[List['TeamMember']] = relationship(back_populates='country', cascade='all, delete-orphan')
    clients: Mapped[List['Client']] = relationship(back_populates='country', cascade='all, delete-orphan')


# ── Пользователи ─────────────────────────────────────────────────────────────
class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_role: Mapped[RoleChoices] = mapped_column(
        Enum(RoleChoices, create_constraint=False),
        default=RoleChoices.client
    )
    registered_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tokens: Mapped[List['RefreshToken']] = relationship(back_populates='token_user', cascade='all, delete-orphan')
    contact_requests: Mapped[List['ContactRequest']] = relationship(back_populates='user', cascade='all, delete-orphan')


# ── Категории услуг ──────────────────────────────────────────────────────────
class ServiceCategory(Base):
    __tablename__ = 'service_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    icon: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    services: Mapped[List['Service']] = relationship(back_populates='category', cascade='all, delete-orphan')


# ── Услуги ───────────────────────────────────────────────────────────────────
class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('service_category.id'))

    category: Mapped['ServiceCategory'] = relationship(back_populates='services')
    projects: Mapped[List['Project']] = relationship(back_populates='service', cascade='all, delete-orphan')


# ── Члены команды ────────────────────────────────────────────────────────────
class TeamMember(Base):
    __tablename__ = 'team_member'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(200))
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey('country.id'), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    country: Mapped[Optional['Country']] = relationship(back_populates='team_members')


# ── Клиенты ──────────────────────────────────────────────────────────────────
class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(200))
    logo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey('country.id'), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)

    country: Mapped[Optional['Country']] = relationship(back_populates='clients')
    projects: Mapped[List['Project']] = relationship(back_populates='client', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='client', cascade='all, delete-orphan')


# ── Проекты (портфолио) ──────────────────────────────────────────────────────
class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    cover_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    project_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey('client.id'), nullable=True)
    status: Mapped[ProjectStatusChoices] = mapped_column(
        Enum(ProjectStatusChoices, create_constraint=False),
        default=ProjectStatusChoices.in_progress
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    service: Mapped['Service'] = relationship(back_populates='projects')
    client: Mapped[Optional['Client']] = relationship(back_populates='projects')
    images: Mapped[List['ProjectImage']] = relationship(back_populates='project', cascade='all, delete-orphan')


# ── Изображения проектов ─────────────────────────────────────────────────────
class ProjectImage(Base):
    __tablename__ = 'project_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'))
    image_url: Mapped[str] = mapped_column(String)
    caption: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    project: Mapped['Project'] = relationship(back_populates='images')


# ── Отзывы клиентов ──────────────────────────────────────────────────────────
class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    author_name: Mapped[str] = mapped_column(String(200))
    author_position: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    author_photo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client: Mapped['Client'] = relationship(back_populates='reviews')


# ── Заявки на контакт ────────────────────────────────────────────────────────
class ContactRequest(Base):
    __tablename__ = 'contact_request'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subject: Mapped[str] = mapped_column(String(300))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[ContactStatusChoices] = mapped_column(
        Enum(ContactStatusChoices, create_constraint=False),
        default=ContactStatusChoices.new
    )
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_profile.id'), nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[Optional['UserProfile']] = relationship(back_populates='contact_requests')


# ── Блог / Статьи ────────────────────────────────────────────────────────────
class BlogPost(Base):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(300), unique=True)
    preview_text: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    cover_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# ── Токены обновления ────────────────────────────────────────────────────────
class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    token_user: Mapped['UserProfile'] = relationship(back_populates='tokens')
