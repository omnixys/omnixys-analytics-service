# src/kpi/router/export_router.py

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from kpi.models.enum.export_format_enum import ExportFormat
from kpi.services.export_service import KpiExportService


router = APIRouter(prefix="/export")


@router.get("/kpis", response_class=FileResponse)
async def get_kpi_export(format: ExportFormat = Query(default=ExportFormat.excel)):
    service = KpiExportService()
    filename = await service.export_all_kpis(format.value)
    return FileResponse(
        path=f"exports/{filename}",
        filename=filename,
        media_type="application/octet-stream",
    )
