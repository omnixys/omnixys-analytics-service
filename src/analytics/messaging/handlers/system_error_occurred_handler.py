# analytics/kafka/handlers/system_error_occurred.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.system_kpi import SystemKPI


@kafka_handler("kpi.create.orchestrator")
async def handle_system_error_occurred(payload: dict):
    dt = datetime.fromisoformat(payload["timestamp"])
    system = await SystemKPI.get_or_create(dt.year, dt.month)
    system.error_count += 1
    system.total_requests += 1
    await system.save()
