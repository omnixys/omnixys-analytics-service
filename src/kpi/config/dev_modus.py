"""Konfiguration für den Entwicklungsmodus."""

from typing import Final

from kpi.config.config import kpi_config

__all__ = ["dev"]


_dev_toml: Final = kpi_config.get("dev", {})

dev: Final[bool] = bool(_dev_toml.get("enabled", False))
"""Flag, ob der Entwicklungsmodus aktiviert ist."""
