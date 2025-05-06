-- psql --dbname=bitnami_keycloak --username=bn_keycloak --file=/sql/kpi/create-db-kpi.sql
-- psql --dbname=kpi_db --username=kpi_db_user --file=/sql/kpi/create-schema-kpi.sql


CREATE ROLE kpi_db_user LOGIN PASSWORD 'GentleCorp16.04.2025';

CREATE DATABASE kpi_db;

GRANT ALL ON DATABASE kpi_db TO kpi_db_user;

CREATE TABLESPACE kpispace OWNER kpi_db_user LOCATION '/var/lib/postgresql/tablespace/kpi';
