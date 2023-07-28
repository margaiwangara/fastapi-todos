from fastapi import APIRouter
from models import CreateUserRequest, User

router = APIRouter()


@router.post("/auth/register")
async def create_user(user: CreateUserRequest):
    new_user = User(
       name=user.name,
       email=user.email,
       password=user.password,
       is_active=True,
       role=user.role,
    )

    return new_user
