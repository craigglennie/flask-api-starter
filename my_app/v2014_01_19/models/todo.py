from sqlalchemy import Column, String, Boolean

from my_app.v2014_01_19.models.base import Base, ModelBase

class ToDo(Base, ModelBase):
    __tablename__ = 'todos'

    text = Column(String, nullable=False)
    is_done = Column(Boolean, nullable=False, default=False)
