from pydantic import BaseModel


class ColumnBase(BaseModel):
    name: str


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(ColumnBase):
    pass


class ColumnOut(ColumnBase):
    id: int
    board_id: int

    class Config:
        orm_mode = True
