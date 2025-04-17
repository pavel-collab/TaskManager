from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.db import Base
from app.utils.utils import Role


class ProjectMembers(Base):
    __tablename__ = 'project_members'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(Enum(Role), default=Role.DEVELOPER)
