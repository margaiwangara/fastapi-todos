import datetime

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from pydantic import BaseModel, Field


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=func.now())


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=5, max_length=50)
    email: str
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@app.com",
                "password": "JohnDoe1",
                "role": "user"
            }
        }


class LoginUserRequest(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@app.com",
                "password": "JohnDoe1"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class TodoRequest(BaseModel):

    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=200)
    priority: int = Field(ge=0)
    complete: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Get milk, eggs, bread, and vegetables from the supermarket",
                "priority": 3,
                "complete": False
            }
        }
