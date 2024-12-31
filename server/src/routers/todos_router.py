from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from ..db import DB

router: APIRouter = APIRouter(prefix="/todos")
db: DB = DB.get_instance()


class InsertTodoModel(BaseModel):
    body: str
    done: bool


@router.get("/fetch/all")
def fetch_all_todos():
    todos = db.fetch_all_todos()

    if todos is None:
        return HTTPException(500, "Could not fetch todos from db")

    return JSONResponse(todos)


@router.get("/fetch/id/{id}")
def fetch_todo_by_id(id: int):
    todo = db.fetch_todo_by_id(id)

    if todo is None:
        return HTTPException(500, "Could not fetch todo from db")

    return JSONResponse(todo)


@router.post("/insert")
def insert_todo(todo: InsertTodoModel):
    new_todo = db.insert_todo(todo.body, todo.done)

    if new_todo is None:
        return HTTPException(500, "Could not insert todo into db")

    return JSONResponse(new_todo, status_code=201)


@router.put("/toggle/{id}")
def toggle_todo(id: int):
    new_todo = db.toggle_todo(id)

    if new_todo is None:
        return HTTPException(500, "Could not update todo db")

    return JSONResponse(new_todo)


@router.delete("/delete/{id}")
def delete_todo(id: int):
    if db.delete_todo_by_id(id):
        return Response(status_code=200)

    return HTTPException(500, "Could not delete todo from db")
