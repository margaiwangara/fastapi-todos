from fastapi import APIRouter, Depends, HTTPException
from models import CreateUserRequest, User, Token
from passlib.context import CryptContext
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime

router = APIRouter()

SECRET_KEY = "e707e2c1ccf145fd2592d9bc321e2150d1436ecc42eec71351a489c374a602ec"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


def authenticate_user(email: str, password: str, db: DB_DEPENDENCY):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: DB_DEPENDENCY, user: CreateUserRequest):
    hashed_password = bcrypt_context.hash(user.password)

    new_user = User(
       name=user.name,
       email=user.email,
       password=hashed_password,
       is_active=True,
       role=user.role,
    )

    db.add(new_user)
    db.commit()


@router.post("/auth/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(db: DB_DEPENDENCY, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(400, "Invalid email or password")

    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    return {
        "access_token": token,
        "token_type": "Bearer"
    }
