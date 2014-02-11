from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from my_app.v2014_01_19.models.base import Base, ModelBase

user_teams = Table('user_teams', Base.metadata,
                   Column('team_id', Integer, ForeignKey('teams.id')),
                   Column('user_id', Integer, ForeignKey('users.id'))
)

class Team(Base, ModelBase):
    __tablename__ = 'teams'

    name = Column(String, nullable=False)
    users = relationship("User",
                        secondary=user_teams,
                        backref="teams")

