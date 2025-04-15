from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Схема для создания проекта
class ProjectCreate(BaseModel):
    title: str
    description: str
    owner_id: int
    status: str
    project_start_date: str
    project_end_date: str
    
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Функция для добавления нового проекта
@router.post("/projects/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(title=project.title, 
                          description=project.description, 
                          owner_id=project.owner_id,
                          status=project.status,
                          project_start_date=project.project_start_date,
                          project_end_date=project.project_end_date)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"message": "Project created", "project": new_project}

# Функция для получения всех проектов
@router.get("/projects/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

# Функция для получения конкретного проекта по id
@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Функция для обновления проекта
@router.put("/projects/{project_id}")
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update project fields if they are provided
    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return {"message": "Project updated", "project": db_project}

# Функция для удаления проекта
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}