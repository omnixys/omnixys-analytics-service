# analytics/kafka/handlers/invoice_overdue.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.invoice_kpi import InvoiceKPI


@kafka_handler("kpi.delete.invoice")
async def handle_invoice_overdue(payload: dict):
    dt = datetime.fromisoformat(payload["dueDate"])
    inv = await InvoiceKPI.get_or_create(dt.year, dt.month)
    inv.overdue_invoices += 1
    await inv.save()
