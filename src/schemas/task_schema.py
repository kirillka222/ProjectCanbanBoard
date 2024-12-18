from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = datetime.utcnow() + timedelta(days=3)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    column_id: int

    class Config:
        orm_mode = True
