from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from kpi.models.entities.base import Base


class CustomerKPI(Base):
    """Entity-Klasse für Kunden-KPIs (Registrierung, Abmeldung)."""

    __tablename__ = "customer_kpis"

    user_id: Mapped[str] = mapped_column(String(64), index=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime)
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    deregistered_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
