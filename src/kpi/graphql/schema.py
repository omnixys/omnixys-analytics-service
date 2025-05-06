from typing import Final, List

import strawberry
from fastapi import Request
from kpi.config.graphql import graphql_ide
from kpi.dependency_provider import get_kpi_query_resolver
from kpi.models.enum.export_format_enum import ExportFormat
from kpi.security.keycloak_service import KeycloakService
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from kpi.services.export_service import KpiExportService


# Kontextbereitstellung
async def get_context(request: Request) -> dict:
    resolver = await get_kpi_query_resolver()
    return {
        "request": request,
        "keycloak": KeycloakService(request),
        "resolver": resolver,
    }


# ---------------------------
# GraphQL Query Definition
# ---------------------------
@strawberry.type
class Query:


    @strawberry.field
    async def export_kpis(self, info: Info, format: ExportFormat = ExportFormat.excel) -> str:
        return await info.context["resolver"].resolve_export_kpis(None, format)

    @strawberry.field
    async def export_kpis_date(self, info: Info, startDate: str, endDate: str, format: ExportFormat = ExportFormat.excel) -> str:
        return "hallo"

    @strawberry.field
    async def total_customers(self, info: Info) -> int:
        return await info.context["resolver"].resolve_total_customers(info)

    @strawberry.field
    async def new_customers(self, info: Info, year: int, month: int) -> int:
        return await info.context["resolver"].resolve_new_customers(info, year, month)

    @strawberry.field
    async def user_spending(self, info: Info, user_id: str) -> float:
        return await info.context["resolver"].resolve_user_spending(info, user_id)

    @strawberry.field
    async def transaction_count(self, info: Info, year: int, month: int) -> int:
        return await info.context["resolver"].resolve_transaction_count(
            info, year, month
        )

    @strawberry.field
    async def transaction_volume(self, info: Info, year: int, month: int) -> float:
        return await info.context["resolver"].resolve_transaction_volume(
            info, year, month
        )


# ---------------------------
# GraphQL Mutation Definition
# ---------------------------


# ---------------------------
# Schema + Router
# ---------------------------
schema = strawberry.Schema(query=Query)

graphql_router: Final = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphql_ide=graphql_ide,
)
