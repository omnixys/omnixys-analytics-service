# analytics/kafka/handlers/account_registered.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.customer_growth_kpi import CustomerGrowthKPI


@kafka_handler("kpi.create.person")
async def handle_account_registered(payload: dict, headers: dict):
    dt = datetime.fromisoformat(payload["createdAt"])
    growth = await CustomerGrowthKPI.get_or_create(dt.year, dt.month)
    growth.new_customers += 1
    await growth.save()
