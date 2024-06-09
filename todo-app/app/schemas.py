from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass
