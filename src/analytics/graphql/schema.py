from typing import Final

from strawberry.federation import Schema
from fastapi import Request
from analytics.config.graphql import graphql_ide
from analytics.graphql.mutation import Mutation
from strawberry.fastapi import GraphQLRouter

from analytics.graphql.query import Query


# Kontextbereitstellung
async def get_context(request: Request) -> dict:
    return {
        "request": request,
        "keycloak": getattr(request.state, "keycloak", None),
    }


# ---------------------------
# GraphQL Query Definition
# ---------------------------

# ---------------------------
# GraphQL Mutation Definition
# ---------------------------


# ---------------------------
# Schema + Router
# ---------------------------
schema = Schema(
    query=Query,
    # mutation=Mutation,
    enable_federation_2=True,
)

graphql_router: Final = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphql_ide=graphql_ide,
)
