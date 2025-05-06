"""Konfiguration für Excel."""

from typing import Final

from kpi.config.config import kpi_config

__all__ = ["excel_enabled"]


_excel_toml: Final = kpi_config.get("excel", {})

excel_enabled: Final[bool] = bool(_excel_toml.get("enabled", False))
"""Flag, ob Excel benutzt werden soll (default: False)."""
