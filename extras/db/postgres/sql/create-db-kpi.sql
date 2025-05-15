-- psql --dbname=bitnami_keycloak --username=bn_keycloak --file=/sql/analytics/create-db-analytics.sql
-- psql --dbname=analytics_db --username=analytics_db_user --file=/sql/analytics/create-schema-analytics.sql


CREATE ROLE analytics_db_user LOGIN PASSWORD 'GentleCorp16.04.2025';

CREATE DATABASE analytics_db;

GRANT ALL ON DATABASE analytics_db TO analytics_db_user;

CREATE TABLESPACE analyticsspace OWNER analytics_db_user LOCATION '/var/lib/postgresql/tablespace/analytics';
