from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo, TodoRequest
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def get_all_todos(user: USER_DEPENDENCY, db: DB_DEPENDENCY):
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized Access")

    return db.query(Todo).filter(Todo.user_id == user.get("id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_single_todo(user: USER_DEPENDENCY, db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized Access")

    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first()

    if todo is None:
        raise HTTPException(404, "Todo not found")

    return todo


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: USER_DEPENDENCY, todo: TodoRequest, db: DB_DEPENDENCY):

    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized Access")
    todo_item = Todo(**todo.model_dump(), user_id=user.get("id"))

    db.add(todo_item)
    db.commit()
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: USER_DEPENDENCY, db: DB_DEPENDENCY, todo: TodoRequest, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized Access")

    todo_item = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first()

    if todo_item is None:
        raise HTTPException(404, "Todo not found")

    todo_item.title = todo.title
    todo_item.description = todo.description
    todo_item.priority = todo.priority
    todo_item.complete = todo.complete

    db.add(todo_item)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: USER_DEPENDENCY, db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized Access")

    todo_item = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first();

    if todo_item is None:
        raise HTTPException(404, "Todo not found")

    db.delete(todo_item)
    db.commit()
