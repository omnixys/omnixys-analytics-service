# 📄 src/analytics/messaging/kafka_handler_registration.py

import importlib
import pkgutil
from analytics.messaging.decorator.kafka_handler_registry import set_dispatcher
import analytics.messaging.handlers  # ✅ korrektes Package
from analytics.messaging.kafka_event_dispatcher import KafkaEventDispatcher
from loguru import logger


def register_kafka_handlers(dispatcher: KafkaEventDispatcher):
    set_dispatcher(dispatcher)

    package = analytics.messaging.handlers  # ⬅️ wichtig!
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name.endswith("_handler"):  # ⬅️ angepasst an deinen Dateinamen
            import_path = f"{package.__name__}.{module_name}"
            logger.debug(f"📦 Importiere Handler-Modul: {import_path}")
            importlib.import_module(import_path)

    logger.info(f"✅ Registrierte Kafka-Topics: {dispatcher.list_topics()}")
