# src/kpi/models/enum/export_format_enum.py

from enum import Enum
import strawberry


@strawberry.enum
class ExportFormat(Enum):
    csv = "csv"
    excel = "excel"
