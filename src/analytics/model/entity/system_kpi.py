# analytics/models/system_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class SystemKPIType(BaseKPIType):
    error_count: int
    total_requests: int


class SystemKPI(BaseKPI):
    error_count: int = 0
    total_requests: int = 0

    @property
    def system_error_rate(self):
        return self.error_count / self.total_requests if self.total_requests else 0

    class Settings:
        name = "system_kpis"
