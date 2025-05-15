from typing import Callable, Awaitable, Any

from loguru import logger


class KafkaEventDispatcher:
    def __init__(self):
        self._handlers: dict[str, Callable[[dict, dict], Awaitable[Any]]] = {}

    def register(self, topic: str, handler: Callable[[dict, dict], Awaitable[Any]]):
        self._handlers[topic] = handler
        # logger.info(
        #     f"📡 Kafka-Handler registriert für Topic: '{topic}' → {handler.__module__}.{handler.__name__}"
        # )

    def get_handler(self, topic: str) -> Callable[[dict, dict], Awaitable[Any]] | None:
        return self._handlers.get(topic)

    def list_topics(self) -> list[str]:
        return list(self._handlers.keys())
