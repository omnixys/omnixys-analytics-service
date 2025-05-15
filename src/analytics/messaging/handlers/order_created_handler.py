# analytics/kafka/handlers/order_created.handler.py
from datetime import datetime

from analytics.messaging.decorator.kafka_handler_registry import kafka_handler
from analytics.model.entity.order_kpi import OrderKPI
from analytics.model.entity.revenue_kpi import RevenueKPI


@kafka_handler("kpi.create.order")
async def handle_order_created(payload: dict):
    dt = datetime.fromisoformat(payload["createdAt"])
    revenue = await RevenueKPI.get_or_create(dt.year, dt.month)
    order = await OrderKPI.get_or_create(dt.year, dt.month)

    revenue.total_revenue += payload["totalAmount"]
    order.total_orders += 1
    order.basket_size_sum += payload["products"]
    order.order_value_sum += payload["totalAmount"]

    await revenue.save()
    await order.save()
