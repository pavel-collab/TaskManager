from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus
from app.db import get_db

router = APIRouter()

@router.post("/tasks/")
def create_task(title: str, description: str, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description, status=TaskStatus.TODO)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "task": new_task}