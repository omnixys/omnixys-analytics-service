from kpi.repositories.kpi_repository import KPIRepository


class KPIReadService:
    """Service-Klasse zur Bereitstellung von lesenden KPI-Operationen."""

    def __init__(self, repository: KPIRepository) -> None:
        self._repository = repository

    async def get_total_customers(self) -> int:
        return await self._repository.count_customers()

    async def get_new_customers_for_month(self, year: int, month: int) -> int:
        return await self._repository.count_new_customers_in_month(year, month)

    async def get_user_total_spending(self, user_id: str) -> float:
        return await self._repository.sum_user_spending(user_id)

    async def get_transaction_count(self, year: int, month: int) -> int:
        return await self._repository.count_transactions_in_month(year, month)

    async def get_transaction_volume(self, year: int, month: int) -> float:
        return await self._repository.sum_transactions_volume(year, month)
