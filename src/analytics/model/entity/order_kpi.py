# analytics/models/order_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class OrderKPIType(BaseKPIType):
    total_orders: int
    basket_size_sum: float
    order_value_sum: float


class OrderKPI(BaseKPI):
    total_orders: int = 0
    basket_size_sum: float = 0.0
    order_value_sum: float = 0.0

    @property
    def avg_basket_size(self):
        return self.basket_size_sum / self.total_orders if self.total_orders else 0

    @property
    def avg_order_value(self):
        return self.order_value_sum / self.total_orders if self.total_orders else 0

    class Settings:
        name = "order_kpis"
