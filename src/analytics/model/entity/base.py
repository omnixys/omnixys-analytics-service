from uuid import UUID, uuid4
from beanie import Document
from datetime import datetime

from pydantic import Field
import strawberry


@strawberry.type
class BaseKPIType:
    id: strawberry.ID | None
    year: int
    month: int


class BaseKPI(Document):
    id: UUID = Field(default_factory=uuid4)
    year: int
    month: int

    class Settings:
        use_state_management = True

    @classmethod
    async def get_or_create(cls, year: int, month: int):
        instance = await cls.find_one({"year": year, "month": month})
        if not instance:
            instance = cls(year=year, month=month)
            await instance.insert()
        return instance
