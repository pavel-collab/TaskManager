from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.db import get_db
from utils.utils import Role
from models.project_members import ProjectMembers
from pydantic import BaseModel

router = APIRouter(
    prefix="/project-members",
    tags=["project-members"],
)


class ProjectMemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: Role = Role.DEVELOPER

class ProjectMemberUpdate(BaseModel):
    role: Role

class ProjectMemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: Role

    class Config:
        orm_mode = True

@router.post("/", response_model=ProjectMemberResponse, status_code=status.HTTP_201_CREATED)
def add_project_member(
    member: ProjectMemberCreate, 
    db: Session = Depends(get_db)
):
    """
    Add a new member to a project with specified role.
    """
    db_member = ProjectMembers(
        project_id=member.project_id,
        user_id=member.user_id,
        role=member.role
    )
    
    try:
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this project or project/user doesn't exist"
        )


@router.get("/project/{project_id}", response_model=List[ProjectMemberResponse])
def get_project_members(
    project_id: int, 
    role: Optional[Role] = None,
    db: Session = Depends(get_db)
):
    """
    Get all members of a specific project with optional role filtering.
    """
    query = db.query(ProjectMembers).filter(ProjectMembers.project_id == project_id)
    
    if role:
        query = query.filter(ProjectMembers.role == role)
    
    members = query.all()
    return members


@router.get("/user/{user_id}", response_model=List[ProjectMemberResponse])
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all projects a user is a member of.
    """
    members = db.query(ProjectMembers).filter(ProjectMembers.user_id == user_id).all()
    return members


@router.put("/{project_id}/{user_id}", response_model=ProjectMemberResponse)
def update_project_member(
    project_id: int,
    user_id: int,
    member_update: ProjectMemberUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a project member's role.
    """
    db_member = db.query(ProjectMembers).filter(
        ProjectMembers.project_id == project_id,
        ProjectMembers.user_id == user_id
    ).first()
    
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project member not found"
        )
    
    db_member.role = member_update.role
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a member from a project.
    """
    db_member = db.query(ProjectMembers).filter(
        ProjectMembers.project_id == project_id,
        ProjectMembers.user_id == user_id
    ).first()
    
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project member not found"
        )
    
    db.delete(db_member)
    db.commit()
    return None