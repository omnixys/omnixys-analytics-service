"""HealthRouter: Liveness- und Readiness-Probe für Kubernetes etc."""

from typing import Any, Final
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from loguru import logger

from kpi.repositories.async_session import get_async_session

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness", tags=["Health"])
def liveness() -> dict[str, Any]:
    """Überprüfen der Liveness (immer 'up').

    :return: JSON-Datensatz mit der Erfolgsmeldung
    """
    return {"status": "up"}


@router.get("/readiness", tags=["Health"])
async def readiness() -> dict[str, str]:
    """Überprüfen der Readiness, d. h. ob die DB erreichbar ist.

    :return: JSON-Datensatz mit DB-Status
    """
    status: Final = "up" if await check_db_connection() else "down"
    return {"db": status}


async def check_db_connection() -> bool:
    """Prüft, ob die Verbindung zur DB funktioniert."""
    try:
        async with get_async_session() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as error:
        logger.warning("Datenbankverbindung fehlgeschlagen: {}", error)
        return False
