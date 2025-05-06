"""Konfiguration für GraphQL."""

from typing import Final

from kpi.config.config import kpi_config
from strawberry.http.ides import GraphQL_IDE

__all__ = ["graphql_ide"]


_graphql_toml: Final = kpi_config.get("graphql", {})
_graphiql_enabled: Final = bool(_graphql_toml.get("graphiql-enabled", False))

graphql_ide: Final[GraphQL_IDE | None] = "graphiql" if _graphiql_enabled else None
"""String 'graphiql', falls GraphiQL aktiviert ist, sonst None."""
