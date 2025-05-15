# analytics/kafka/handlers/payment_completed.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.transaction_kpi import TransactionKPI


@kafka_handler("kpi.create.payment")
async def handle_payment_completed(payload: dict):
    dt = datetime.fromisoformat(payload["timestamp"])
    txn = await TransactionKPI.get_or_create(dt.year, dt.month)
    txn.transaction_volume += payload["amount"]
    await txn.save()
