from sqlalchemy import Integer, ForeignKey, Column, String, Boolean
from sqlalchemy.orm import relationship

from my_app.v2014_01_19.models.base import Base, ModelBase

class Task(Base, ModelBase):
    __tablename__ = 'tasks'

    text = Column(String, nullable=False)
    is_done = Column(Boolean, nullable=False, default=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team = relationship("Team", backref="tasks")

