"""
Modul-Deklaration für das Projekt als Namensraum und CLI-Einstiegspunkt.

Ermöglicht:
- Import als Python-Package: `from analytics import ...`
- Ausführung als Skript: `uv run analytics`
- Start per Uvicorn/Hypercorn z.B.:

    uvicorn src.analytics:app --reload --ssl-keyfile path --ssl-certfile path
"""

from analytics.asgi_server import run
from analytics.fastapi_app import app

__all__ = ["app", "main"]


def main() -> None:
    """Einstiegspunkt für CLI-Aufrufe via `uv run analytics`."""
    run()
