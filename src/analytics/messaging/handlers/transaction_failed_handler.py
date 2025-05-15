# analytics/kafka/handlers/transaction_failed.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.transaction_kpi import TransactionKPI


@kafka_handler("kpi.error.transaction")
async def handle_transaction_failed(payload: dict):
    dt = datetime.fromisoformat(payload["timestamp"])
    txn = await TransactionKPI.get_or_create(dt.year, dt.month)
    txn.failed_transactions += 1
    await txn.save()
