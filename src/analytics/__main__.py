"""CLI-Einstiegspunkt für das Projekt, z.B. über `python -m analytics`."""

from analytics.asgi_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
