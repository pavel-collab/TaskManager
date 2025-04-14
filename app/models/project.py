from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from utils.utils import Status
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(Status), default=Status.TODO)
    project_start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    project_end_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # _owner = relationship("User", back_populates="projects")