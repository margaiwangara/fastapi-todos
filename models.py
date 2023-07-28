from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, Field


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


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
