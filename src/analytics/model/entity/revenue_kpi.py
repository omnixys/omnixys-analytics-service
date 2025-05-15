# analytics/models/revenue_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


class RevenueKPI(BaseKPI):
    total_revenue: float = 0.0

    class Settings:
        name = "revenue_kpis"


@strawberry.type
class RevenueKPIType(BaseKPIType):
    total_revenue: float
