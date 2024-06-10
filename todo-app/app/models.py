from typing import List
from pydantic import BaseModel
from .schemas import TodoCreate

class Todo(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

    def __str__(self) -> str:
        return f'Todo({self.title}, {self.description}, {self.completed})'

    class Config:
        orm_mode = True


db = [
        Todo(id=1, title="Learn FastAPI", description="Study FastAPI framework", completed=False),
        Todo(id=2, title="Build API", description="Build an API with FastAPI", completed=False),
    ]

def get_db():
    return db
