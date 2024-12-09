from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BoardBase(BaseModel):
    user_id: int
    user_name: str
    description: Optional[str] = None


class BoardCreate(BoardBase):
    pass


class BoardOut(BoardBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
