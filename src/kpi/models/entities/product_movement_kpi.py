from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from kpi.models.entities.base import Base


class MovementType(str, Enum):
    """Typ der Produktbewegung: Einkauf oder Verkauf."""

    PURCHASED = "PURCHASED"
    SOLD = "SOLD"


class ProductMovementKPI(Base):
    """Entity-Klasse für Produktbewegungen (Ein-/Verkauf)."""

    __tablename__ = "product_movement_kpis"

    product_id: Mapped[str] = mapped_column(String(64))
    movement_type: Mapped[MovementType] = mapped_column(SqlEnum(MovementType))
    quantity: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
