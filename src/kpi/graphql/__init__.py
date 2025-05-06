"""Modul für die GraphQL-Schnittstelle."""

from kpi.graphql.schema import Query, graphql_router

__all__ = [
    "Query",
    "graphql_router",
]
