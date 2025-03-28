from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.task import Task, TaskStatus
from app.models.project import Project
from pydantic import BaseModel

router = APIRouter()

# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: str
    status: TaskStatus
    project_id: int

# Функция для добавления новой задачи
@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли проект для этой задачи
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    new_task = Task(title=task.title, description=task.description, status=task.status, project_id=task.project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "task": new_task}

# Функция для получения всех задач
@router.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# Функция для получения конкретной задачи по id
@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task