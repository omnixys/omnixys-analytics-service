import json
from typing import Final, Optional
from aiokafka import AIOKafkaProducer
from loguru import logger

from kpi.config.kafka import get_kafka_settings
from kpi.models.dto import (
    CustomerCreatedPayload,
    OrderCompletedPayload,
    TransactionCreatedPayload,
    ProductMovementPayload,
)


class KafkaProducerService:
    """Kafka Producer für KPI-relevante Events."""

    def __init__(self) -> None:
        self._producer: Optional[AIOKafkaProducer] = None
        self._logger = logger.bind(classname=self.__class__.__name__)
        self._settings = get_kafka_settings()
        self._topics = {
            "customer.created": self._settings.topic_customer_created,
            "order.completed": self._settings.topic_order_completed,
            "transaction.created": self._settings.topic_transaction_created,
            "product.moved": self._settings.topic_product_moved,
        }

    async def start(self) -> None:
        """Initialisiere Kafka Producer asynchron."""
        if self._producer is None:
            self._logger.info("Starte Kafka Producer...")
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._settings.bootstrap_servers,
                client_id="kpi-service",
                acks="all",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self._producer.start()

    async def stop(self) -> None:
        """Stoppe Kafka Producer."""
        if self._producer:
            self._logger.info("Stoppe Kafka Producer...")
            await self._producer.stop()
            self._producer = None

    async def publish_customer_created(self, payload: CustomerCreatedPayload) -> None:
        await self._send("customer.created", payload.model_dump())

    async def publish_order_completed(self, payload: OrderCompletedPayload) -> None:
        await self._send("order.completed", payload.model_dump())

    async def publish_transaction_created(
        self, payload: TransactionCreatedPayload
    ) -> None:
        await self._send("transaction.created", payload.model_dump())

    async def publish_product_moved(self, payload: ProductMovementPayload) -> None:
        await self._send("product.moved", payload.model_dump())

    async def _send(self, topic_key: str, message: dict) -> None:
        if self._producer is None:
            raise RuntimeError("Kafka Producer wurde nicht gestartet.")
        topic = self._topics.get(topic_key)
        if topic is None:
            raise ValueError(f"Unbekannter Topic-Key: {topic_key}")
        self._logger.debug("Sende Event an %s: %s", topic, message)
        await self._producer.send_and_wait(topic, message)
