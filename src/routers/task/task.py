from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.crud.task_crud import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)
from src.routers.auth.utils import get_current_user
from src.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    column_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_task(db, task, column_id)


@router.get("/", response_model=list[TaskOut])
def get_all_tasks(
    column_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_tasks(db, column_id, skip, limit)


@router.get("/{task_id}", response_model=TaskOut)
def get_single_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return db_task


@router.put("/{task_id}", response_model=TaskOut)
def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_task = update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    if not delete_task(db, task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return
