from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

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

#TODO: добавить каскадное удаление соответствующих сущностей
# Функция для удаления проекта
@router.delete("/projects/{project_title}")
def delete_project(project_title: str, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.title == project_title).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}

@router.get("/ranked-projects")
def get_ranked_projects(db: Session = Depends(get_db)) -> List[dict]:
    now = datetime.utcnow()

    projects = db.query(Project).all()

    def project_priority(project: Project):
        if project.project_start_date and project.project_start_date > now:
            return 0  # проект ещё не начался

        if not project.project_end_date:
            return 0.1  # без дедлайна — почти минимальный приоритет

        hours_left = (project.project_end_date - now).total_seconds() / 3600
        hours_left = max(1, hours_left)

        return round((1 / hours_left) * 100, 2)

    projects.sort(key=project_priority, reverse=True)

    ranked_result = [
        {
            "id": project.id,
            "name": project.title,
            "start_date": project.project_start_date,
            "end_date": project.project_end_date,
            "priority_score": project_priority(project)
        }
        for project in projects
    ]

    return ranked_result