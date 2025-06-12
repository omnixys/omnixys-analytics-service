# analytics/messaging/kafka_singleton.py

from typing import Optional
from analytics.config import env
from analytics.messaging.kafka_consumer_service import KafkaConsumerService
from analytics.messaging.kafka_event_dispatcher import KafkaEventDispatcher
from analytics.messaging.kafka_handler_registration import register_kafka_handlers
from analytics.messaging.kafka_producer_service import KafkaProducerService
from analytics.messaging.kafka_topic_properties import KafkaTopics

# ❌ Kein @lru_cache, damit .start()/.stop() steuerbar bleiben
_kafka_producer_instance: Optional[KafkaProducerService] = None
_kafka_consumer_instance: Optional[KafkaConsumerService] = None


def get_kafka_producer() -> KafkaProducerService:
    global _kafka_producer_instance
    if _kafka_producer_instance is None:
        _kafka_producer_instance = KafkaProducerService()
    return _kafka_producer_instance


dispatcher = KafkaEventDispatcher()
register_kafka_handlers(dispatcher)


async def get_kafka_consumer() -> KafkaConsumerService:
    return KafkaConsumerService(
        dispatcher=dispatcher,
        topics=dispatcher.list_topics(),
        bootstrap_servers=env.KAFKA_URI,
    )
