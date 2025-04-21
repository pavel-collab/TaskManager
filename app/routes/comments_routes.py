from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from pydantic import BaseModel
from app.models.comments import TaskComments

# Pydantic models for request/response


class TaskCommentBase(BaseModel):
    task_id: int
    user_id: int
    comment: str


class TaskCommentCreate(TaskCommentBase):
    pass


class TaskCommentUpdate(BaseModel):
    comment: str


class TaskCommentResponse(TaskCommentBase):
    id: int
    comment_date: datetime

    class Config:
        orm_mode = True


# Router
router = APIRouter()


@router.post('/comments', response_model=TaskCommentResponse,
             status_code=status.HTTP_201_CREATED)
def create_comment(comment: TaskCommentCreate, db: Session = Depends(get_db)):
    """Create a new task comment."""
    db_comment = TaskComments(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get('/comments/{comment_id}', response_model=TaskCommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    """Get a specific comment by ID."""
    db_comment = db.query(TaskComments).filter(
        TaskComments.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail='Comment not found')
    return db_comment

# TODO: вот тут точно можно использовать id задачи как параметр запроса, а
# не как часть запроса


@router.get('/comments/task/{task_id}',
            response_model=List[TaskCommentResponse])
def read_comments_by_task(task_id: int, db: Session = Depends(get_db)):
    """Get all comments for a specific task."""
    comments = db.query(TaskComments).filter(
        TaskComments.task_id == task_id).all()
    return comments


@router.put('/comments/{comment_id}', response_model=TaskCommentResponse)
def update_comment(comment_id: int, comment: TaskCommentUpdate,
                   db: Session = Depends(get_db)):
    """Update a comment."""
    db_comment = db.query(TaskComments).filter(
        TaskComments.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail='Comment not found')

    update_data = comment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)

    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete('/comments/{comment_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete a comment."""
    db_comment = db.query(TaskComments).filter(
        TaskComments.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail='Comment not found')

    db.delete(db_comment)
    db.commit()
    return None
