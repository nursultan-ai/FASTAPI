from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, RefreshToken
from mysite.database.schema import UserRegister, UserLoginSchema, TokenResponse, RefreshTokenRequest
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from mysite.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(UserProfile).filter(UserProfile.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username уже занят!")
    if db.query(UserProfile).filter(UserProfile.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован!")

    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=get_password_hash(user.password),
        user_role=user.user_role,
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Регистрация прошла успешно!'}


@auth_router.post('/login', response_model=TokenResponse)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail='Неверные данные!')

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    db.add(RefreshToken(user_id=user_db.id, token=refresh_token))
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/logout')
async def logout(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()
    if not stored:
        raise HTTPException(status_code=401, detail='Токен не найден!')
    db.delete(stored)
    db.commit()
    return {'message': 'Вышли из системы!'}


@auth_router.post('/refresh')
async def refresh(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()
    if not stored:
        raise HTTPException(status_code=401, detail='Токен не найден!')
    access_token = create_access_token({'sub': stored.user_id})
    return {'access_token': access_token, 'token_type': 'Bearer'}
