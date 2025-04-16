from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.task import Task
from app.utils.utils import Status
from app.models.project import Project
from pydantic import BaseModel

router = APIRouter()

# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: str
    status: Status
    project_id: int
    complexity: str
    assign_id: int
    task_start_date: str
    task_end_date: str

# Функция для добавления новой задачи
@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли проект для этой задачи
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    new_task = Task(title=task.title, 
                    description=task.description, 
                    status=task.status, 
                    project_id=task.project_id,
                    complexity=task.complexity,
                    assign_id=task.assign_id,
                    task_start_date=task.task_start_date,
                    task_end_date=task.task_end_date)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "task": new_task}

# Функция для получения всех задач
@router.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

#TODO: изменить: получить задачу по названию
# Функция для получения конкретной задачи по id
@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#TODO: сделать так, чтобы можно было вносить частичные изменения
# Функция для обновления задачи
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    """
    Update an existing task by ID.
    
    Args:
        task_id: The ID of the task to update
        task_update: The new task data
        db: Database session
        
    Returns:
        Updated task information
        
    Raises:
        HTTPException: If task not found or project not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == task_update.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Find and update the task
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task fields
    task.title = task_update.title
    task.description = task_update.description
    task.status = task_update.status
    task.project_id = task_update.project_id
    
    db.commit()
    db.refresh(task)
    return {"message": "Task updated", "task": task}

#TODO: добавить каскадное удаление соответствующих сущностей
# Функция для удаления задачи
@router.delete("/tasks/{task_title}")
def delete_task(task_title: str, db: Session = Depends(get_db)):
    """
    Delete a task by ID.
    
    Args:
        task_id: The ID of the task to delete
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(Task).filter(Task.title == task_title).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}