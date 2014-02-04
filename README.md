# flask-api-starter

A starter-kit for a RESTful API built with Flask. 

## Features
- Support for multiple endpoint versions (useful for long-lived APIs)
- Schema changes managed by Alembic and run automatically as part of unit tests
- Multiple configurations (testing, staging, production, etc...)
- Basic Postgres configuration with a schema, API user, and migrations user
- All DB migrations are run before every unit-test; ensures migrations are working

## Built With
flask-api-starter is mostly plumbing, all credit should go to the excellent packages it builds on:
- REST API: [flask-restful](http://flask-restful.readthedocs.org)
- POST validation and ORM mapping: [WTForms-JSON](http://wtforms-json.readthedocs.org/) and [WTForms-Alchemy](http://wtforms-alchemy.readthedocs.org/)
- Database migrations: [Alembic](http://alembic.readthedocs.org/)
- Testing fixtures: [factory_boy](https://factoryboy.readthedocs.org/)
- Web framework: [Flask](http://flask.readthedocs.org)
- ORM: [SQLAlchemy](http://docs.sqlalchemy.org/)
