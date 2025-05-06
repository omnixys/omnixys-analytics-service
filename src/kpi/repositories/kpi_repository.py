from datetime import datetime

from kpi.models.entities import CustomerKPI, OrderKPI, TransactionKPI
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from kpi.models.entities.product_movement_kpi import ProductMovementKPI


class KPIRepository:
    """Repository-Klasse zur Abfrage von KPIs aus verschiedenen Entitäten."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_customers(self) -> int:
        stmt = select(func.count()).select_from(CustomerKPI)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_new_customers_in_month(self, year: int, month: int) -> int:
        stmt = (
            select(func.count())
            .select_from(CustomerKPI)
            .where(
                func.extract("year", CustomerKPI.registered_at) == year,
                func.extract("month", CustomerKPI.registered_at) == month,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def sum_user_spending(self, user_id: str) -> float:
        stmt = select(func.sum(OrderKPI.total_price)).where(OrderKPI.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0.0

    async def count_transactions_in_month(self, year: int, month: int) -> int:
        stmt = (
            select(func.count())
            .select_from(TransactionKPI)
            .where(
                func.extract("year", TransactionKPI.created_at) == year,
                func.extract("month", TransactionKPI.created_at) == month,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def sum_transactions_volume(self, year: int, month: int) -> float:
        stmt = select(func.sum(TransactionKPI.amount)).where(
            func.extract("year", TransactionKPI.created_at) == year,
            func.extract("month", TransactionKPI.created_at) == month,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0.0

    async def find_all_customer_kpis(self) -> list[CustomerKPI]:
        stmt = select(CustomerKPI)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_transaction_kpis(self) -> list[TransactionKPI]:
        stmt = select(TransactionKPI)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_order_kpis(self) -> list[OrderKPI]:
        stmt = select(OrderKPI)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_product_movement_kpis(self) -> list[ProductMovementKPI]:
        stmt = select(ProductMovementKPI)
        result = await self.session.execute(stmt)
        return result.scalars().all()
