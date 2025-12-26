"""
Factories for new types.
"""

from collections import deque
from collections.abc import Callable
from typing import Any, Deque, Generic, TypeVar
from uuid import UUID

from .lastuuid import uuid7

__all__ = [
    "NewTypeFactory",
    "LastUUIDFactory",
]


T = TypeVar("T", bound=UUID)


class NewTypeFactory(Generic[T]):
    """
    Factory for NewType UUIDs
    """

    def __init__(self, newtype: Any, id_factory: Callable[[], UUID] = uuid7):
        """
        Create a factory of type that store the last instances.

        :param newtype: the type to be used
        :param id_factory: the factory to use, uuid7 by default.
        """
        self._newtype = newtype
        self._id_factory = id_factory

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Generate a new value."""
        val = self._id_factory(*args, **kwargs)  # type: ignore
        if self._newtype:
            val: T = self._newtype(val)  # cast to NewType
        return val


class LastUUIDFactory(NewTypeFactory[T]):
    """
    Keep last UUID generated.

    ```python
    >>> from typing import NewType
    >>> from uuid import UUID
    >>> from lastuuid.utils import LastUUIDFactory
    >>> ClientId = NewType("ClientId", UUID)
    >>> client_id_factory = LastUUIDFactory[ClientId](ClientId)
    >>> client_id_factory()
    UUID('019b4f7d-f9d1-7d46-922a-7b83c4462366')
    >>> client_id_factory()
    UUID('019b4f7d-f9d2-7471-b6bb-c48f31146c56')
    >>> client_id_factory()
    UUID('019b4f7d-f9d2-7471-b6bb-c490f5b50e3a')
    >>> client_id_factory.last
    UUID('019b4f7d-f9d2-7471-b6bb-c490f5b50e3a')
    >>> client_id_factory.lasts[0]
    UUID('019b4f7d-f9d2-7471-b6bb-c490f5b50e3a')
    >>> client_id_factory.lasts[1]
    UUID('019b4f7d-f9d2-7471-b6bb-c48f31146c56')
    >>> client_id_factory.lasts[2]
    UUID('019b4f7d-f9d1-7d46-922a-7b83c4462366')
    ```
    """
    def __init__(
        self,
        newtype: Any,
        id_factory: Callable[[], UUID] = uuid7,
        cache_size: int = 10,
    ):
        """
        Create a factory of type that store the last instances.

        :param newtype: the type to be used
        :param cache_size: size of the queue that saved the last uuids
        """
        super().__init__(newtype, id_factory)
        self._cache: Deque[T] = deque(maxlen=cache_size)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Generate the id and cache it."""
        val = super().__call__(*args, **kwargs)
        self._cache.append(val)
        return val

    @property
    def last(self) -> T:
        """Most recently generated UUID-NewType instance."""
        return self._cache[-1]

    @property
    def lasts(self) -> list[T]:
        """
        Returns a list of the last N generated UUID-NewType instances.

        The list is ordered from most recent to oldest.
        The most recent value is accessible via `last`.
        """
        return list(reversed(self._cache))
