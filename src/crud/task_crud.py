from sqlalchemy.orm import Session
from src.models.task import Task
from src.schemas.task_schema import TaskCreate, TaskUpdate



def create_task(db: Session, task: TaskCreate, column_id: int) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        column_id=column_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, column_id: int, skip: int = 0, limit: int = 10) -> list[Task]:
    return db.query(Task).filter(Task.column_id == column_id).offset(skip).limit(limit).all()



def get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()



def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.title = task_data.title
        db_task.description = task_data.description
        db_task.deadline = task_data.deadline
        db.commit()
        db.refresh(db_task)
    return db_task



def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
