from fastapi import APIRouter
from models import CreateUserRequest, User
from passlib.context import CryptContext
from starlette import status

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest):
    hashed_password = bcrypt_context.hash(user.password)

    new_user = User(
       name=user.name,
       email=user.email,
       password=hashed_password,
       is_active=True,
       role=user.role,
    )

    return new_user
