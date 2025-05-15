"""
MongoDB-Verbindung initialisieren für Beanie + Motor.
"""

from typing import Final

from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from analytics.config import env
from analytics.model.entity.customer_growth_kpi import CustomerGrowthKPI
from analytics.model.entity.invoice_kpi import InvoiceKPI
from analytics.model.entity.order_kpi import OrderKPI
from analytics.model.entity.revenue_kpi import RevenueKPI
from analytics.model.entity.support_kpi import SupportKPI
from analytics.model.entity.system_kpi import SystemKPI
from analytics.model.entity.transaction_kpi import TransactionKPI


__all__ = ["init_mongo"]

# Konfiguration aus der .env via pydantic-settings
MONGO_DB_URI: Final[str] = env.MONGO_DB_URI
MONGO_DB_DATABASE: Final[str] = env.MONGO_DB_DATABASE

# Der globale Client kann bei Bedarf wiederverwendet werden
client: Final = AsyncIOMotorClient(MONGO_DB_URI)


async def init_mongo() -> None:
    """
    Initialisiert die Verbindung zur MongoDB und registriert Beanie-Modelle.
    Wird beim Startup ausgeführt.
    """
    logger.info("🔌 Initialisiere MongoDB-Client mit URI {}", MONGO_DB_URI)

    await init_beanie(
        database=client[MONGO_DB_DATABASE],
        document_models=[
            RevenueKPI,
            CustomerGrowthKPI,
            OrderKPI,
            TransactionKPI,
            InvoiceKPI,
            SupportKPI,
            SystemKPI,
        ],
    )

    logger.success(
        "✅ MongoDB-Initialisierung abgeschlossen (DB: {})", MONGO_DB_DATABASE
    )
