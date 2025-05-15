# analytics/models/customer_growth_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class CustomerGrowthKPIType(BaseKPIType):
    new_customers: int


class CustomerGrowthKPI(BaseKPI):
    new_customers: int = 0

    class Settings:
        name = "customer_growth_kpis"
