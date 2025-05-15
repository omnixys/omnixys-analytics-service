from loguru import logger
from analytics.config import dev
from analytics.config.dev.source_raw_kpi_entries import RAW_KPI_ENTRIES
from analytics.model.entity.revenue_kpi import RevenueKPI
from analytics.model.entity.customer_growth_kpi import CustomerGrowthKPI
from analytics.model.entity.order_kpi import OrderKPI
from analytics.model.entity.transaction_kpi import TransactionKPI
from analytics.model.entity.invoice_kpi import InvoiceKPI
from analytics.model.entity.support_kpi import SupportKPI
from analytics.model.entity.system_kpi import SystemKPI


MODEL_MAP = {
    "RevenueKPI": RevenueKPI,
    "CustomerGrowthKPI": CustomerGrowthKPI,
    "OrderKPI": OrderKPI,
    "TransactionKPI": TransactionKPI,
    "InvoiceKPI": InvoiceKPI,
    "SupportKPI": SupportKPI,
    "SystemKPI": SystemKPI,
}


async def mongo_populate():
    """
    Füllt MongoDB mit Testdaten (nur im DEV-Modus).
    Löscht vorher bestehende KPI-Daten.
    """
    if not dev:
        logger.warning("⚠️ DEV-Modus ist deaktiviert. Seed wird übersprungen.")
        return

    logger.warning(">>> MongoDB wird im DEV-Modus befüllt <<<")

    # Bestehende KPI-Daten löschen
    for model_cls in MODEL_MAP.values():
        deleted = await model_cls.find_all().delete()
        logger.info(f"🗑️  {deleted} Einträge aus {model_cls.__name__} gelöscht")

    # Neue Testdaten einfügen
    for entry in RAW_KPI_ENTRIES:
        model_cls = MODEL_MAP[entry["model"]]
        obj = model_cls(**entry["data"])
        await obj.insert()

    logger.success("✅ KPI-Testdaten erfolgreich eingefügt.")
