from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()

# 데이터 저장 파일
DATA_FILE = Path("todos.json")

# Pydantic 모델
class Todo(BaseModel):
    id: int = None
    title: str
    completed: bool = False
    created_at: str = None

# 초기 데이터 로드
def load_todos():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 데이터 저장
def save_todos(todos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# 모든 할 일 조회
@app.get("/api/todos")
async def get_todos():
    return load_todos()

# 새 할 일 추가
@app.post("/api/todos")
async def create_todo(todo: Todo):
    todos = load_todos()
    
    # ID 생성 (가장 큰 ID + 1)
    new_id = max([t["id"] for t in todos], default=0) + 1
    
    new_todo = {
        "id": new_id,
        "title": todo.title,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    save_todos(todos)
    
    return new_todo

# 할 일 완료 상태 변경
@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    todos = load_todos()
    
    for t in todos:
        if t["id"] == todo_id:
            t["completed"] = todo.completed
            t["title"] = todo.title
            save_todos(todos)
            return t
    
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

# 할 일 삭제
@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todos = load_todos()
    
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            deleted = todos.pop(i)
            save_todos(todos)
            return {"message": "삭제되었습니다", "deleted_todo": deleted}
    
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 메인 페이지
@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
