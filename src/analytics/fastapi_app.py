"""MainApp."""

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Final

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from analytics.config import dev, env
from analytics.config.dev.db_populate import mongo_populate
from analytics.config.mongo import init_mongo
from analytics.config.otel_setup import setup_otel
from analytics.error.exceptions import NotAllowedError, NotFoundError, VersionOutdatedError
from analytics.graphql.schema import graphql_router
from analytics.messaging.kafka_producer_service import KafkaProducerService
from analytics.messaging.kafka_singleton import get_kafka_consumer, get_kafka_producer
from analytics.security.keycloak_service import KeycloakService

from analytics.health.router import router as health_router

from .banner import banner

__all__ = [
    "authorization_error_handler",
    "email_exists_error_handler",
    "login_error_handler",
    "not_allowed_error_handler",
    "not_found_error_handler",
    "username_exists_error_handler",
    "version_outdated_error_handler",
]


TEXT_PLAIN: Final = "text/plain"
kafka_producer = KafkaProducerService()

# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """Startup/Shutdown-Logik: MongoDB, Kafka, Banner."""
    await init_mongo()
    kafka_consumer = await get_kafka_consumer()
    kafka_producer = get_kafka_producer()

    logger.info("Starte Kafka Producer…")
    await kafka_producer.start()
    await kafka_consumer.start()
    if dev:
        await mongo_populate()
    banner(app.routes)
    yield

    logger.info("← Shutting down services…")
    await kafka_producer.stop()
    await kafka_consumer.stop()
    logger.info("Der Server wird heruntergefahren")

if env.APP_ENV == "development":
    app: Final = FastAPI(lifespan=lifespan, debug=True)
else:
    app: Final = FastAPI(lifespan=lifespan)


# --------------------------------------------------------------------------------------
# M I D D L E W A R E
# --------------------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder ["http://localhost:3000"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def inject_keycloak(request: Request, call_next):
    # Sonderfall: Introspection oder kein Token
    try:
        body = await request.body()
        if b"__schema" in body or b"__introspection" in body:
            request.state.keycloak = None
            return await call_next(request)
    except Exception:
        request.state.keycloak = None
        return await call_next(request)

    # Normale Authentifizierung
    try:
        request.state.keycloak = await KeycloakService.create(request)
    except HTTPException as e:
        logger.warning("Keycloak Token-Fehler: {}", e.detail)
        request.state.keycloak = None  # sicherstellen, dass Attribut gesetzt ist

    return await call_next(request)


# Setup Observability
setup_otel(app)  # Tracing mit Tempo
Instrumentator().instrument(app).expose(app)  # Prometheus-Metriken
# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(health_router)


# --------------------------------------------------------------------------------------
# G r a p h Q L
# --------------------------------------------------------------------------------------
app.include_router(graphql_router, prefix="/graphql")

# --------------------------------------------------------------------------------------
# F a v i c o n
# --------------------------------------------------------------------------------------
@app.get("/favicon.ico")
def favicon() -> FileResponse:
    """facicon.ico ermitteln.

    :return: Response-Objekt mit favicon.ico
    :rtype: FileResponse
    """
    src_path: Final = Path("src")
    file_name: Final = "favicon.ico"
    favicon_path: Final = Path("analytics") / "static" / file_name
    file_path: Final = src_path / favicon_path if src_path.is_dir() else favicon_path
    logger.debug("file_path={}", file_path)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------
@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError.

    :param _err: NotFoundError aus der Geschäftslogik
    :return: Response mit Statuscode 404
    :rtype: Response
    """
    return Response(status_code=status.HTTP_404_NOT_FOUND, media_type=TEXT_PLAIN)


@app.exception_handler(NotAllowedError)
def not_allowed_error_handler(_request: Request, _err: NotAllowedError) -> Response:
    """Errorhandler für NotAllowedError.

    :param _err: NotAllowedError vom Überprüfen der erforderlichen Rollen
    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return Response(status_code=status.HTTP_401_UNAUTHORIZED, media_type=TEXT_PLAIN)


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    _err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError.

    :param _err: Exception, falls die Versionsnummer zum Aktualisieren veraltet ist
    :return: Response mit Statuscode 412
    :rtype: Response
    """
    return Response(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        media_type="application/json",
    )
