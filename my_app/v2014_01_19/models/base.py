from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, DateTime

from my_app.app import app

__all__ = ["session", "ModelBase", "Base"]

Base = declarative_base()

with app.app_context():
    engine = create_engine(app.config["DB_URI"])

@app.teardown_appcontext
def teardown_db(exception):
    session.close()

session = scoped_session(sessionmaker(bind=engine, autoflush=False))

class ModelBase(object):
    query = session.query_property()

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    @classmethod
    def by_id(cls, id):
        return cls.query.filter(cls.id==id).first()

# Automatically add new Model objects to the session,
# this avoids having to call session.add(new_object)
def auto_add(target, args, kwargs):
    session.add(target)
event.listen(ModelBase, 'init', auto_add, propagate=True)





