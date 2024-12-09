from sqlalchemy.orm import Session
from src.models.board import Board
from src.schemas.schemas_board import BoardCreate

# Создать доску
def create_board(db: Session, board: BoardCreate):
    db_board = Board(**board.dict())
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

# Получить все доски
def get_boards(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Board).offset(skip).limit(limit).all()

# Получить доску по ID
def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()

# Обновить доску
def update_board(db: Session, board_id: int, updated_data: dict):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if db_board:
        for key, value in updated_data.items():
            setattr(db_board, key, value)
        db.commit()
        db.refresh(db_board)
    return db_board

# Удалить доску
def delete_board(db: Session, board_id: int):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if db_board:
        db.delete(db_board)
        db.commit()
    return db_board
