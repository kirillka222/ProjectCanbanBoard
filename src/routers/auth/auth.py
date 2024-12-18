from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import insert, delete, update

from src.schemas import UserInDB, TokenData, Token
from src.routers.auth.utils import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
)
from sqlalchemy.orm import Session
from fastapi import Depends
from src.core.db import get_db
from src.models.user import User
from src.schemas.auth_scheme import User as PydanticUser
from .utils import get_password_hash

router = APIRouter(prefix="/demo_auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/create", status_code=204)
def create_user(db: Annotated[Session, Depends(get_db)], user: PydanticUser):
    db.execute(
        insert(User).values(
            user_name=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            full_name=user.full_name,
        )
    )

    db.commit()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.user_name}]


@router.delete("/users/delete/{userID}")
def delete_user(db: Annotated[Session, Depends(get_db)], userID: int):
    db.execute(delete(User).where(User.id == userID))
    db.commit()
    return f"Пользователь удалён {userID}"


@router.put("/users/put/{userID}")
def put_user(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    userID: int,
    user_scheme: PydanticUser,
):
    db.execute(
        update(User)
        .where(User.id == userID)
        .values(user_name=user_scheme.username, email=user_scheme.email)
    )
    db.commit()
    return {"msg": f"Успешно обновлено {userID}"}


# get post put delete.
