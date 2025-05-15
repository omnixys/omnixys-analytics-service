# analytics/models/invoice_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class InvoiceKPIType(BaseKPIType):
    invoices_issued: int
    overdue_invoices: int


class InvoiceKPI(BaseKPI):
    invoices_issued: int = 0
    overdue_invoices: int = 0

    class Settings:
        name = "invoice_kpis"
