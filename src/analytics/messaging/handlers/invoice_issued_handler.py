# analytics/kafka/handlers/invoice_issued.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.invoice_kpi import InvoiceKPI


@kafka_handler("kpi.create.invoice")
async def handle_invoice_issued(payload: dict):
    dt = datetime.fromisoformat(payload["issuedAt"])
    inv = await InvoiceKPI.get_or_create(dt.year, dt.month)
    inv.invoices_issued += 1
    await inv.save()
