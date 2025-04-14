from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from utils.utils import Status, Complexity
from datetime import datetime
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(Status), default=Status.TODO)
    project_id = Column(Integer, ForeignKey("projects.id"))
    complexity = Column(Enum(Complexity), default=Complexity.LOW)
    assign_id = Column(Integer, ForeignKey("users.id"))
    task_start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    task_end_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # _project = relationship("Project", back_populates="tasks")
    