"""Basisklasse für alle SQLAlchemy-Entity-Klassen."""

from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:

    class MappedAsDataclass:
        """PEP 681-kompatibles Mixin für Typing-Unterstützung."""

        def __init__(self, *args: Any, **kwargs: Any) -> None: ...

else:
    from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Basisklasse für alle Entity-Klassen mit Unterstützung für @dataclass."""
