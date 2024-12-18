from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.crud.column_crud import (
    create_column,
    get_columns,
    get_column,
    update_column,
    delete_column,
)
from src.routers.auth.utils import get_current_user
from src.schemas.column_schema import ColumnCreate, ColumnUpdate, ColumnOut

router = APIRouter(prefix="/columns", tags=["Columns"])


@router.post("/", response_model=ColumnOut, status_code=status.HTTP_201_CREATED)
def create_new_column(
    column: ColumnCreate,
    board_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_column(db, column, board_id)


@router.get("/", response_model=list[ColumnOut])
def get_all_columns(
    board_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_columns(db, board_id, skip, limit)


@router.get("/{column_id}", response_model=ColumnOut)
def get_single_column(
    column_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_column = get_column(db, column_id)
    if not db_column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Column not found"
        )
    return db_column


@router.put("/{column_id}", response_model=ColumnOut)
def update_existing_column(
    column_id: int,
    column: ColumnUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_column = update_column(db, column_id, column)
    if not db_column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Column not found"
        )
    return db_column


@router.delete("/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_column(
    column_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not delete_column(db, column_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Column not found"
        )
    return
