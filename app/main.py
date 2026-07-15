from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db, init_db
from app import schemas, crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/api/todos")
def list_todos(status: str = "all", db: Session = Depends(get_db)):
    if status not in {"all", "active", "completed"}:
        raise HTTPException(status_code=422, detail="잘못된 상태 값입니다")
    todos = crud.get_todos(db=db, status=status)
    return [schemas.TodoResponse.model_validate(todo).model_dump() for todo in todos]


@app.post("/api/todos", status_code=201)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = crud.create_todo(db=db, title=payload.title)
    return schemas.TodoResponse.model_validate(todo).model_dump()


@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo_completion(db=db, todo_id=todo_id, completed=payload.completed)
    if todo is None:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")
    return schemas.TodoResponse.model_validate(todo).model_dump()


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db=db, todo_id=todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")
