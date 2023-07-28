from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todo, TodoRequest
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}


@app.get("/todos")
async def get_all_todos(db: DB_DEPENDENCY):
    return db.query(Todo).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_single_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is not None:
        return todo
    raise HTTPException(404, "Todo not found")


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: DB_DEPENDENCY):
    todo_item = Todo(**todo.model_dump())

    db.add(todo_item)
    db.commit()
    return todo


@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first();

    if todo_item is None:
        raise HTTPException(404, "Todo not found")

    db.delete(todo_item)
    db.commit()
