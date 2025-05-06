"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from kpi.router.health_router import liveness, readiness
from kpi.router.export_route import router as export_router
from kpi.router.health_router import router as health_router
from kpi.router.shutdown_router import router as shutdown_router
from kpi.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "delete_by_id",
    "get",
    "get_by_id",
    "get_nachnamen",
    "health_router",
    "export_router",
    "liveness",
    "patient_get_router",
    "patient_write_router",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
