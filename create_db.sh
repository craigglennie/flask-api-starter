#!/bin/bash
set -xe

sudo -u postgres psql -c "DROP OWNED BY migrations"
sudo -u postgres psql -c "DROP OWNED BY my_app"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS my_app"
sudo -u postgres psql -c "DROP USER IF EXISTS my_app"
sudo -u postgres psql -c "DROP USER IF EXISTS migrations"

sudo -u postgres psql -c "CREATE DATABASE my_app"

sudo -u postgres psql -c "CREATE USER migrations WITH PASSWORD 'password'"
sudo -u postgres psql -c "GRANT CONNECT, TEMPORARY ON DATABASE my_app TO migrations"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO migrations"

sudo -u postgres psql -c "CREATE USER my_app WITH PASSWORD 'password'"
sudo -u postgres psql -c "GRANT CONNECT, TEMPORARY ON DATABASE my_app TO my_app"

# Connect to 'my_app' database and alter the default privileges
# for tables and sequences created by the 'migrations' user to allow the 'my_app'
# user to access them. The 'public' schema is a Postgres default
# schema that all databases have (they may also have custom schemas).
# Use of 'ALTER DEFAULT' rather than 'GRANT [...]' means that we don't
# have to GRANT privileges to 'my_app' each time 'migrations' creates a new
# table.
sudo -u postgres psql --dbname=my_app -c "SET ROLE migrations; ALTER DEFAULT PRIVILEGES IN SCHEMA PUBLIC GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO my_app;"
sudo -u postgres psql --dbname=my_app -c "SET ROLE migrations; ALTER DEFAULT PRIVILEGES IN SCHEMA PUBLIC GRANT USAGE ON SEQUENCES TO my_app;"
