from typing import Annotated
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI, Depends, status
from src.routers.auth.auth import router as auth_router
from src.core.db import get_db
from src.schemas.auth_scheme import User
from src.models.user import User as UserDB
from sqlalchemy import insert
from src.core.db import Base, engine
from src.models import User, Columns, Board, Task
from src.routers.board.board import router as router_board
from src.routers.column.column import router as router_column
from src.routers.task.task import router as router_task


Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(router_board)
app.include_router(router_column)
app.include_router(router_task)

@app.get("/Hello")
def sayHello():
    return {'MEASSAGE':"Hello"}


# @app.post("/create_user")
# def create_user(db: Annotated[Session, Depends(get_db)], user: User):
#     db.execute(insert(UserDB).values(user_name=user.username,
#                                          email=user.email,
#                                          hashed_password=user.password,
#                                          full_name=user.full_name,
#                                          ))
#
#     db.commit()
#     return {
#         "status_code": status.HTTP_201_CREATED,
#         "detail": "User added"
#     }