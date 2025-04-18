from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.db import Base


class TaskComments(Base):
    __tablename__ = 'task_comments'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    comment = Column(String)
    comment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
