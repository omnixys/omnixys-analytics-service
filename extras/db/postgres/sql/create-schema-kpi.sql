    --    psql --dbname=bitnami_keycloak --username=bn_keycloak --file=/sql/analytics/create-db-analytics.sql
    --    psql --dbname=analytics_db --username=analytics_db_user --file=/sql/analytics/create-schema-analytics.sql

CREATE SCHEMA IF NOT EXISTS analytics_schema AUTHORIZATION analytics_db_user;

ALTER ROLE analytics_db_user SET search_path = 'analytics_schema';
