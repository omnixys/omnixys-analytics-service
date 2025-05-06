from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"

    topic_kpi_created: str = "kpi.created"
    topic_customer_created: str = "customer.created"
    topic_order_completed: str = "order.completed"
    topic_transaction_created: str = "transaction.created"
    topic_product_moved: str = "product.moved"

    class Config:
        env_prefix = "KAFKA_"


def get_kafka_settings() -> KafkaSettings:
    return KafkaSettings()
