HOST='0.0.0.0'
DEBUG=True

DB_URI="postgresql://my_app:password@127.0.0.1/my_app"
DB_MIGRATIONS_URI="postgresql://migrations:password@127.0.0.1/my_app"
# Setting SERVER_NAME "enables URL generation without a request
# context but with an application context." This is used by the
# unit tests.
# SERVER_NAME = "localhost"
