"""Konfiguration für synchronen SQLAlchemy-Zugriff (z. B. für db_populate)."""

from sqlalchemy.engine import URL
from typing import Final
from loguru import logger

from kpi.config.config import kpi_config
from kpi.config.db import db_dialect

__all__ = ["db_url_sync", "db_url_admin_sync"]

_db_toml: Final = kpi_config.get("db", {})

_name: Final[str] = _db_toml.get("name", "kpi")
_main_memory: Final[bool] = bool(_db_toml.get("main-memory", False))
_host: Final[str] = _db_toml.get("host", db_dialect)
_db_host: Final[str] = _host if _host != "postgresql" else "postgres"
_username: Final[str] = _db_toml.get("username", "kpi")
_password: Final[str] = _db_toml.get("password", "Change Me!")
_password_admin: Final[str] = _db_toml.get("password-admin", "Change Me!")
_username_admin: Final[str] = _db_toml.get("username-admin", "Change Me!")

# Hauptverbindung (Nutzer: kpi)
db_url_sync: Final = URL.create(
    drivername="postgresql+psycopg",
    username=_username,
    password=_password,  # 🔐 aus secrets oder .env laden empfohlen
    host=_host,
    database=_name,
)

# Admin-Verbindung (z. B. für COPY, CSV-Import etc.)
db_url_admin_sync: Final = URL.create(
    drivername="postgresql+psycopg",
    username=_username_admin,
    password=_password_admin,
    host=_host,
    database=_name,
)

logger.debug("db_url_sync: {}", db_url_sync)
logger.debug("db_url_admin_sync: {}", db_url_admin_sync)
