# analytics/models/support_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class SupportKPIType(BaseKPIType):
    total_orders: int
    basket_size_sum: float
    order_value_sum: float


class SupportKPI(BaseKPI):
    support_requests: int
    avg_response_time_total: float
    request_count: int

    @property
    def avg_response_time(self):
        return (
            self.avg_response_time_total / self.request_count
            if self.request_count
            else 0
        )

    class Settings:
        name = "support_kpis"
