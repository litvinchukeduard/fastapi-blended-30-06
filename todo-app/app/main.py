from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from .models import Todo, get_db
from .schemas import TodoCreate, TodoUpdate

app = FastAPI()

@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate, db: List[Todo] = Depends(get_db)):
    # db.append(todo)
    # print('hello')
    # return todo
    todo_model = Todo(id=len(db) + 1, title=todo.title, description=todo.description, completed=todo.completed)
    db.append(todo_model)
    return todo_model

@app.get("/todos/", response_model=List[Todo])
def read_todos(skip: int = 0, limit: int = 10, db: List[Todo] = Depends(get_db)):
    return db[skip:skip + limit]

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db: List[Todo] = Depends(get_db)):
    for todo in db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: List[Todo] = Depends(get_db)):
    print(todo)
    for index, t in enumerate(db):
        if t.id == todo_id:
            print(t)
            db[index].title = todo.title
            db[index].description = todo.description if todo.description else db[index].description
            if todo.completed:
                db[index].completed = todo.completed
            return db[index]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int, db: List[Todo] = Depends(get_db)):
    for index, t in enumerate(db):
        if t.id == todo_id:
            return db.pop(index)
    raise HTTPException(status_code=404, detail="Todo not found")

# uvicorn app.main:app --reload
