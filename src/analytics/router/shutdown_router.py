"""REST-Schnittstelle für Shutdown."""

import os
import signal
from typing import Any, Final

from fastapi import APIRouter, Depends
from loguru import logger

__all__ = ["router"]


router: Final = APIRouter(tags=["Admin"])


# "Dependency Injection" durch Depends
@router.post("/shutdown")
def shutdown() -> dict[str, Any]:
    """Der Server wird heruntergefahren."""
    logger.warning("Server shutting down without calling cleanup handlers.")
    os.kill(os.getpid(), signal.SIGINT)  # NOSONAR
    return {"message": "Server is shutting down..."}
