from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class TaskStatus(enum.Enum):
    #TODO: we can also add more statuses
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="tasks")
    