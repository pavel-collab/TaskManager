from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.db import Base
from utils.utils import Role
from datetime import datetime

class TaskComments(Base):
    __tablename__ = "task_comments"
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String)
    comment_date = Column(DateTime, nullable=False, default=datetime.utcnow)