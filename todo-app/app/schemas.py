from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str = None
    completed: bool = False

    def __str__(self) -> str:
        return f'{self.title}, {self.description}, {self.completed}'

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass
