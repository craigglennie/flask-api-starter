from sqlalchemy import Table, Column, String, Boolean, Unicode, DateTime, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship

from my_app.v2014_01_19.models.base import Base, ModelBase

class User(Base, ModelBase):
    __tablename__ = 'users'

    active = Column(Boolean, nullable=False, default=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    confirmed_at = Column(DateTime, nullable=True)

role_actions = Table('role_actions', Base.metadata,
    Column('action_id', Integer, ForeignKey('actions.id'), nullable=False, primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), nullable=False, primary_key=True)
)

class Action(Base, ModelBase):
    """Represents a single action that can be taken by a user,
    for example the CRUD actions 'create', 'retrieve', 'update'
    and 'delete'"""

    __tablename__ = 'actions'
    name = Column(String(50), nullable=False, unique=True)

class Role(Base, ModelBase):
    """A role is a named collection of Actions"""

    __tablename__ = 'roles'
    name = Column(String(50), nullable=False, unique=True)

class UserRoles(Base, ModelBase):
    """Gives a User a Role for an instance of a class

    permissions_for specifies the SQLAlchemy
    Model that the UserRolePermissions applies to

    object_id specifies the ID of the class indicated by
    permissions_for that the UserRolePermissions applies to"""

    __tablename__ = 'user_roles'

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    object_id = Column(Integer, nullable=False)

    permissions_for = None
    inherits_permissions_from = None


