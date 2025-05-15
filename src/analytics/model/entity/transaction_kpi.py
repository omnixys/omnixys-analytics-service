# analytics/models/transaction_kpi.py
import strawberry
from analytics.model.entity.base import BaseKPI, BaseKPIType


@strawberry.type
class TransactionKPIType(BaseKPIType):
    transaction_volume: float
    failed_transactions: int


class TransactionKPI(BaseKPI):
    transaction_volume: float = 0.0
    failed_transactions: int = 0

    class Settings:
        name = "transaction_kpis"
