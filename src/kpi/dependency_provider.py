from kpi.kafka.producer import KafkaProducerService
from kpi.repositories.kpi_repository import KPIRepository
from kpi.repositories.async_session import async_session_factory
from kpi.resolvers.kpi_query_resolver import KPIQueryResolver
from kpi.services.export_service import KpiExportService
from kpi.services.kpi_read_service import KPIReadService

__all__ = ["get_kpi_query_resolver", "get_kafka_producer"]

_kafka_producer: KafkaProducerService | None = None


async def get_kpi_query_resolver() -> KPIQueryResolver:
    """Erzeuge Resolver mit DB-Zugriff und Service."""
    async with async_session_factory() as session:
        repository = KPIRepository(session=session)
        service = KPIReadService(repository=repository)
        export_service = KpiExportService(repository)
        return KPIQueryResolver(
            kpi_read_service=service,
            export_service=export_service,
        )


def get_kafka_producer() -> KafkaProducerService:
    """Singleton-Instanz des Kafka-Producers bereitstellen."""
    global _kafka_producer
    if _kafka_producer is None:
        _kafka_producer = KafkaProducerService()
    return _kafka_producer
