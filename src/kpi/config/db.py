"""DB-URL erstellen."""

from importlib.resources import files
from importlib.resources.abc import Traversable
import ssl
from typing import Final, Literal

from loguru import logger
from sqlalchemy.engine import URL

from kpi.config.config import kpi_config, resources_path

__all__ = [
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
    "db_url_admin",
]

_db_toml: Final = kpi_config.get("db", {})

db_dialect: Final[Literal["postgresql", "mysql", "sqlite"]] = _db_toml.get(
    "dialect",
    "postgresql",
)
"""DB-Dialekt für SQLAlchemy: 'postgresql', 'mysql', 'sqlite'."""
logger.debug("db: db_dialect={}", db_dialect)

_name: Final[str] = _db_toml.get("name", "kpi")
_main_memory: Final[bool] = bool(_db_toml.get("main-memory", False))
_host: Final[str] = _db_toml.get("host", db_dialect)
_db_host: Final[str] = _host if _host != "postgresql" else "postgres"
_username: Final[str] = _db_toml.get("username", "kpi")
_password: Final[str] = _db_toml.get("password", "Change Me!")
_password_admin: Final[str] = _db_toml.get("password-admin", "Change Me!")
_admin_username: Final[str] = _db_toml.get("username-admin", "Change Me!")

db_log_statements: Final[bool] = bool(_db_toml.get("log-statements", False))
"""True, falls die SQL-Anweisungen protokolliert werden sollen."""


__db_resources_traversable: Final[Traversable] = files(resources_path)


def _get_drivername() -> str:
    # "Structural Pattern Matching" ab Python 3.10, https://peps.python.org/pep-0634
    match db_dialect:

        case "postgresql":
            return "postgresql+asyncpg"

        case "mysql":
            return "mysql+pymysql"

        case "sqlite":
            return "sqlite+pysqlite"


def _get_database() -> str:
    if db_dialect == "sqlite":
        if _main_memory:
            return ":memory:"
        return str(__db_resources_traversable / "sqlite" / f"{_name}.sqlite")
    return _name


def _create_db_url() -> URL:
    if db_dialect in {"postgresql", "mysql"}:
        return URL.create(
            drivername=_get_drivername(),
            username=_username,
            password=_password,
            host=_db_host,
            database=_get_database(),
        )

    return URL.create(
        drivername=_get_drivername(),
        database=_get_database(),
    )


def _create_db_url_admin() -> URL:
    if db_dialect in {"postgresql", "mysql"}:
        return URL.create(
            drivername=_get_drivername(),
            username=_admin_username,
            password=_password_admin,
            host=_db_host,
            database=_get_database(),
        )

    return URL.create(
        drivername=_get_drivername(),
        database=_get_database(),
    )


db_url: Final[URL] = _create_db_url()
"""DB-URL für SQLAlchemy."""
logger.debug("db: db_url={}", db_url)

db_url_admin: Final[URL] = _create_db_url_admin()
"""DB-URL für den Superuser für SQLAlchemy."""


def _create_connect_args() -> dict[str, str | dict[str, str]] | None:
    cafile: Final = str(
        __db_resources_traversable / db_dialect / "certificate.crt",
    )

    if db_dialect == "postgresql":
        return {}
    if db_dialect == "mysql":
        return {"ssl": {"ca": cafile}}
    return None


db_connect_args: dict[str, str | dict[str, str]] | None = _create_connect_args()
"""Schlüssel-Wert-Paare für TLS bei PostgreSQL oder MySQL."""
logger.debug("db: db_connect_args={}", db_connect_args)
