from typing import List, Optional, Type, TypeVar
import strawberry
from analytics.graphql.filters import KpiFilter
from analytics.model.entity.customer_growth_kpi import CustomerGrowthKPI, CustomerGrowthKPIType
from analytics.model.entity.invoice_kpi import InvoiceKPI, InvoiceKPIType
from analytics.model.entity.order_kpi import OrderKPI, OrderKPIType
from analytics.model.entity.revenue_kpi import RevenueKPI, RevenueKPIType
from analytics.model.entity.support_kpi import SupportKPI, SupportKPIType
from analytics.model.entity.system_kpi import SystemKPI, SystemKPIType
from analytics.model.entity.transaction_kpi import TransactionKPI, TransactionKPIType


T = TypeVar("T")

def build_filter_query(filter: KpiFilter) -> dict:
    if filter.year and filter.month:
        return {"year": filter.year, "month": filter.month}
    elif filter.year:
        return {"year": filter.year}
    elif filter.from_date and filter.to_date:
        return {
            "$expr": {
                "$and": [
                    {
                        "$gte": [
                            {"$dateFromParts": {"year": "$year", "month": "$month"}},
                            {"$date": filter.from_date.isoformat()},
                        ]
                    },
                    {
                        "$lte": [
                            {"$dateFromParts": {"year": "$year", "month": "$month"}},
                            {"$date": filter.to_date.isoformat()},
                        ]
                    },
                ]
            }
        }
    return {}


async def run_kpi_query(
    model,
    dto_cls: Type[T],
    filter: KpiFilter,
    sort: bool = True,
    limit: Optional[int] = None,
) -> List[T]:
    query = build_filter_query(filter)
    cursor = model.find(query)
    if sort:
        cursor.sort([("year", 1), ("month", 1)])
    if limit:
        cursor.limit(limit)

    results = await cursor.to_list()
    return [dto_cls(**r.dict()) for r in results]


@strawberry.type
class Query:

    @strawberry.field
    async def revenue_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[RevenueKPIType]:
        return await run_kpi_query(RevenueKPI, RevenueKPIType, filter, sort, limit)

    @strawberry.field
    async def customer_growth_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[CustomerGrowthKPIType]:
        return await run_kpi_query(
            CustomerGrowthKPI, CustomerGrowthKPIType, filter, sort, limit
        )

    @strawberry.field
    async def order_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[OrderKPIType]:
        return await run_kpi_query(OrderKPI, OrderKPIType, filter, sort, limit)

    @strawberry.field
    async def transaction_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[TransactionKPIType]:
        return await run_kpi_query(
            TransactionKPI, TransactionKPIType, filter, sort, limit
        )

    @strawberry.field
    async def invoice_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[InvoiceKPIType]:
        return await run_kpi_query(InvoiceKPI, InvoiceKPIType, filter, sort, limit)

    @strawberry.field
    async def support_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[SupportKPIType]:
        return await run_kpi_query(SupportKPI, SupportKPIType, filter, sort, limit)

    @strawberry.field
    async def system_kpis(
        self, filter: KpiFilter, sort: bool = True, limit: Optional[int] = None
    ) -> List[SystemKPIType]:
        return await run_kpi_query(SystemKPI, SystemKPIType, filter, sort, limit)
