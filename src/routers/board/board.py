from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.routers.auth.utils import get_current_user
from src.schemas.schemas_board import BoardCreate, BoardOut
from src.crud.board_crud import (
    create_board,
    get_boards,
    get_board,
    update_board,
    delete_board,
)

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_board(
    board: BoardCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_board(db, board)


@router.get("/")
def get_all_boards(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_boards(db, skip=skip, limit=limit)


@router.get("/{board_id}")
def get_single_board(
    board_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db_board = get_board(db, board_id)
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return db_board


@router.put("/{board_id}")
def update_existing_board(
    board_id: int,
    board: BoardCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_board = update_board(db, board_id, board.dict())
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return db_board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_board(
    board_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db_board = delete_board(db, board_id)
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return
