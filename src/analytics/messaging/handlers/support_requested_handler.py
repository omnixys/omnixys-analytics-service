# analytics/kafka/handlers/support_requested.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.support_kpi import SupportKPI


@kafka_handler("kpi.create.support")
async def handle_support_requested(payload: dict):
    dt = datetime.fromisoformat(payload["timestamp"])
    support = await SupportKPI.get_or_create(dt.year, dt.month)
    support.support_requests += 1
    support.avg_response_time_total += payload["responseTime"]
    support.request_count += 1
    await support.save()
