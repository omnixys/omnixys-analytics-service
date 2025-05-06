"""
Modul-Deklaration für das Projekt als Namensraum und CLI-Einstiegspunkt.

Ermöglicht:
- Import als Python-Package: `from kpi import ...`
- Ausführung als Skript: `uv run kpi`
- Start per Uvicorn/Hypercorn z.B.:

    uvicorn src.kpi:app --reload --ssl-keyfile path --ssl-certfile path
"""

from kpi.asgi_server import run
from kpi.fastapi_app import app

__all__ = ["app", "main"]


def main() -> None:
    """Einstiegspunkt für CLI-Aufrufe via `uv run kpi`."""
    run()
