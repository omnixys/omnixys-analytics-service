"""Synchroner SQLAlchemy-Engine & Session-Fabrik für Admin-Tools."""

from typing import Final
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kpi.config.sync_db import db_url_sync, db_url_admin_sync

__all__ = ["Session", "dispose_connection_pool", "engine", "engine_admin"]

# Main engine (z. B. für Lesetools oder Populatoren)
engine: Final = create_engine(
    db_url_sync,
    echo=True,
)

# Admin engine (z. B. für CSV COPY oder DB-Verwaltung)
engine_admin: Final = create_engine(
    db_url_admin_sync,
    echo=True,
)

Session = sessionmaker(bind=engine, autoflush=False)


def dispose_connection_pool() -> None:
    """Schließt alle offenen DB-Verbindungen und leert den Pool."""
    logger.info("Connection-Pool wird getrennt.")
    engine.dispose()
    engine_admin.dispose()
