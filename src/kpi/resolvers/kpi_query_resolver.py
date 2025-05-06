from kpi.models.enum.export_format_enum import ExportFormat
from kpi.services.export_service import KpiExportService
from kpi.services.kpi_read_service import KPIReadService
from strawberry.types import Info


class KPIQueryResolver:
    """Resolver-Klasse mit Dependency Injection via Konstruktor."""

    def __init__(
        self, kpi_read_service: KPIReadService, export_service: KpiExportService
    ):
        self.kpi_read_service = kpi_read_service
        self.export_service = export_service

    async def resolve_total_customers(self, info: Info) -> int:
        return await self.kpi_read_service.get_total_customers()

    async def resolve_new_customers(
        self, info: Info, year: int = 2025, month: int = 4
    ) -> int:
        return await self.kpi_read_service.get_new_customers_for_month(year, month)

    async def resolve_user_spending(self, info: Info, user_id: str = "") -> float:
        return await self.kpi_read_service.get_user_total_spending(user_id)

    async def resolve_transaction_count(
        self, info: Info, year: int = 2025, month: int = 4
    ) -> int:
        return await self.kpi_read_service.get_transaction_count(year, month)

    async def resolve_transaction_volume(
        self, info: Info, year: int = 2025, month: int = 4
    ) -> float:
        return await self.kpi_read_service.get_transaction_volume(year, month)

    async def resolve_export_kpis(self, info: Info, format: ExportFormat) -> str:
        file_name = await self.export_service.export_all_kpis(format.value)
        return f"/export/export/kpis?file={file_name}"
