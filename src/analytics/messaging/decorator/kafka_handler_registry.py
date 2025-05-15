# src/analytics/messaging/kafka_handler_registry.py

from analytics.messaging.kafka_event_dispatcher import KafkaEventDispatcher
from loguru import logger

_dispatcher: KafkaEventDispatcher | None = None
_buffered_handlers: list[tuple[str, callable]] = []


def set_dispatcher(dispatcher: KafkaEventDispatcher):
    global _dispatcher
    _dispatcher = dispatcher

    for topic, handler in _buffered_handlers:
        _dispatcher.register(topic, handler)
        logger.debug(
            f"🧠 Gepufferter Kafka-Handler registriert: {topic} → {handler.__module__}.{handler.__name__}"
        )


def kafka_handler(topic: str):
    def decorator(func):
        if _dispatcher is not None:
            _dispatcher.register(topic, func)
            logger.debug(
                f"📡 Kafka-Handler registriert: {topic} → {func.__module__}.{func.__name__}"
            )
        else:
            _buffered_handlers.append((topic, func))
            logger.debug(
                f"🕓 Kafka-Handler gepuffert: {topic} → {func.__module__}.{func.__name__}"
            )
        return func

    return decorator
