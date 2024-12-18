from sqlalchemy.orm import Session
from src.models.column import Columns
from src.schemas.column_schema import ColumnCreate, ColumnUpdate


def create_column(db: Session, column: ColumnCreate, board_id: int) -> Columns:
    db_column = Columns(name=column.name, board_id=board_id)
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column


def get_columns(
    db: Session, board_id: int, skip: int = 0, limit: int = 10
) -> list[Columns]:
    return (
        db.query(Columns)
        .filter(Columns.board_id == board_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_column(db: Session, column_id: int) -> Columns:
    return db.query(Columns).filter(Columns.id == column_id).first()


def update_column(db: Session, column_id: int, column_data: ColumnUpdate) -> Columns:
    db_column = db.query(Columns).filter(Columns.id == column_id).first()
    if db_column:
        db_column.name = column_data.name
        db.commit()
        db.refresh(db_column)
    return db_column


def delete_column(db: Session, column_id: int) -> bool:
    db_column = db.query(Columns).filter(Columns.id == column_id).first()
    if db_column:
        db.delete(db_column)
        db.commit()
        return True
    return False
