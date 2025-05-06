from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from kpi.models.entities.base import Base


class OrderKPI(Base):
    """Entity-Klasse für Bestell-KPIs."""

    __tablename__ = "order_kpis"


    user_id: Mapped[str] = mapped_column(String(64), index=True)
    total_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
