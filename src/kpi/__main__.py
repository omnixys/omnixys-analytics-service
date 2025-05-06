"""CLI-Einstiegspunkt für das Projekt, z.B. über `python -m kpi`."""

from kpi.asgi_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
