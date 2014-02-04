import factory
import factory.alchemy

from my_app.v2014_01_19.models import session

class ModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    FACTORY_SESSION = session

    @factory.post_generation
    def flush(self, create, extracted, **kwargs):
        session.commit()

