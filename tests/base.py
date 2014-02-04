import unittest
import urllib
import json

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

from my_app import app
from my_app.v2014_01_19.models import session

class BaseTestCase(unittest.TestCase):
    """Base TestCase running all migrations via Alembic"""

    def setUp(self):
        super(BaseTestCase, self).setUp()
        # Drop all tables and recreate schema by running migrations (this tests
        # migrations)
        with app.app_context():
            self._drop_all_tables()
            config = Config("alembic.ini")
            command.upgrade(config, "head")

        self.client = app.test_client()

    def tearDown(self):
        # Closing the session ensures that we don't have any transactions
        # from the current test interfering with the next
        session.close()

    def _drop_all_tables(self):
        """Reset the test DB to a clean state

        Based on http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything"""
        engine = create_engine(app.config['DB_MIGRATIONS_URI'])
        conn = engine.connect()

        # the transaction only applies if the DB supports
        # transactional DDL, i.e. Postgresql, MS SQL Server
        trans = conn.begin()

        inspector = reflection.Inspector.from_engine(conn.engine)

        # gather all data first before dropping anything.
        # some DBs lock after things have been dropped in
        # a transaction.

        metadata = MetaData()

        tbs = []
        all_fks = []

        for table_name in inspector.get_table_names():
            fks = []
            for fk in inspector.get_foreign_keys(table_name):
                if not fk['name']:
                    continue
                fks.append(
                    ForeignKeyConstraint((),(),name=fk['name'])
                    )
            t = Table(table_name,metadata,*fks)
            tbs.append(t)
            all_fks.extend(fks)

        for fkc in all_fks:
            conn.execute(DropConstraint(fkc))

        for table in tbs:
            conn.execute(DropTable(table))

        trans.commit()

class APITestCase(BaseTestCase):

    def _assert_response_status(self, function, url, expected_status_code, data=None, content_type='application/json'):
        response = function(url, data=data, content_type=content_type)
        if expected_status_code != response.status_code:
            raise AssertionError("URL: %s. Expected status %s != %s. Response:\n%s" % (
                url, expected_status_code, response.status_code, response.data
            ))
        return json.loads(response.data)

    def json_GET(self, url, expect_status_code=200, **kwargs):
        """Helper function for making GETs that return JSON"""
        assert "?" not in url, 'Use **kwargs to pass query string components (found "?" in URL)'
        query_string = urllib.urlencode(kwargs)
        if query_string:
            url = url + "?" + query_string
        return self._assert_response_status(self.client.get, url, expect_status_code)

    def json_POST(self, url, expect_status_code=200, **kwargs):
        """Helper function for making POSTs with JSON content"""
        serialized = json.dumps(kwargs)
        return self._assert_response_status(self.client.post, url, expect_status_code, data=serialized)

    def json_PUT(self, url, expect_status_code=200, **kwargs):
        """Helper function for making PUTs with JSON content"""
        serialized = json.dumps(kwargs)
        return self._assert_response_status(self.client.put, url, expect_status_code, data=serialized)

    def query(self, obj):
        with app.app_context():
            return session.query(obj)

class ResourceTestCase(APITestCase):

    def setUp(self, api, resource):
        super(ResourceTestCase, self).setUp()
        self.url = "%s/%s" % (api.blueprint.name, resource.endpoint)

    def json_GET(self, id=None, expect_status_code=200, **kwargs):
        url = "%s/%s" % (self.url, id) if id else self.url
        return super(ResourceTestCase, self).json_GET(
            url,
            expect_status_code=expect_status_code,
            **kwargs
        )

    def json_POST(self, expect_status_code=200, **kwargs):
        return super(ResourceTestCase, self).json_POST(
            self.url,
            expect_status_code=expect_status_code,
            **kwargs
        )

    def json_PUT(self, id, expect_status_code=200, **kwargs):
        url = "%s/%s" % (self.url, id)
        return super(ResourceTestCase, self).json_PUT(
            url,
            expect_status_code=expect_status_code,
            **kwargs
        )
