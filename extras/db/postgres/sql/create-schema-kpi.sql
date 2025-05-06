    --    psql --dbname=bitnami_keycloak --username=bn_keycloak --file=/sql/kpi/create-db-kpi.sql
    --    psql --dbname=kpi_db --username=kpi_db_user --file=/sql/kpi/create-schema-kpi.sql

CREATE SCHEMA IF NOT EXISTS kpi_schema AUTHORIZATION kpi_db_user;

ALTER ROLE kpi_db_user SET search_path = 'kpi_schema';
