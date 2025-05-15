# # src/kpi/services/kpi_export_service.py
# from pathlib import Path
# from datetime import datetime

# from loguru import logger

# from analytics.repositories.kpi_repository import KPIRepository
# from analytics.utils.export_utils import export_to_csv, export_to_excel


# class KpiExportService:
#     """Exportiert alle KPIs in CSV oder Excel mit Logo & Diagrammen."""

#     def __init__(self, kpi_repository: KPIRepository) -> None:
#         self.kpi_repository = kpi_repository

#     async def export_all_kpis(self, format: str) -> str:
#         logger.debug("export_all_kpis: format={}", format)
#         file_ext = "csv" if format == "csv" else "xlsx"
#         file_name = f"kpis_{datetime.now().strftime('%Y-%m-%d')}.{file_ext}"
#         export_path = Path("exports") / file_name
#         export_path.parent.mkdir(parents=True, exist_ok=True)

#         kpi_data = {
#             "customer_kpis": await self.kpi_repository.find_all_customer_kpis(),
#             "transaction_kpis": await self.kpi_repository.find_all_transaction_kpis(),
#             "order_kpis": await self.kpi_repository.find_all_order_kpis(),
#             "product_movement_kpis": await self.kpi_repository.find_all_product_movement_kpis(),
#         }

#         if format == "csv":
#             export_to_csv(kpi_data, export_path)
#         else:
#             export_to_excel(kpi_data, export_path)

#         return file_name
