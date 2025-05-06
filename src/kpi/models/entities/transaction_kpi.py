from uuid import uuid4
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Float, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from kpi.models.entities.base import Base


class TransactionType(str, Enum):
    """Transaktionstypen für finanzielle Bewegungen."""

    TRANSFER = "TRANSFER"
    PURCHASE = "PURCHASE"


class TransactionKPI(Base):
    """Entity-Klasse für Transaktions-KPIs."""

    __tablename__ = "transaction_kpis"

    user_id: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[float] = mapped_column(Float)
    transaction_type: Mapped[TransactionType] = mapped_column(SqlEnum(TransactionType))
    created_at: Mapped[datetime] = mapped_column(DateTime)

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
