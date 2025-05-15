import strawberry

from analytics.config.dev.db_populate import mongo_populate


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def dev_seed_kpis(self) -> bool:
        await mongo_populate()
        return True
