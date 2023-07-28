from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo, TodoRequest
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@router.get("/todos")
async def get_all_todos(db: DB_DEPENDENCY):
    return db.query(Todo).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_single_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is not None:
        return todo
    raise HTTPException(404, "Todo not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: DB_DEPENDENCY):
    todo_item = Todo(**todo.model_dump())

    db.add(todo_item)
    db.commit()
    return todo


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: DB_DEPENDENCY, todo: TodoRequest, todo_id: int = Path(gt=0)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo_item is None:
        raise HTTPException(404, "Todo not found")

    todo_item.title = todo.title
    todo_item.description = todo.description
    todo_item.priority = todo.priority
    todo_item.complete = todo.complete

    db.add(todo_item)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first();

    if todo_item is None:
        raise HTTPException(404, "Todo not found")

    db.delete(todo_item)
    db.commit()
