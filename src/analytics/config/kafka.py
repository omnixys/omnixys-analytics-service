from pydantic_settings import BaseSettings

from analytics.config import env


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = env.KAFKA_URI
    topic_log: str = "logstream.log.analytics"
    client_id: str = env.PROJECT_NAME

    class Config:
        env_prefix = "KAFKA_"


def get_kafka_settings() -> KafkaSettings:
    return KafkaSettings()
