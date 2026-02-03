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
    >>> from lastuuid.factories import LastUUIDFactory
    >>> ClientId = NewType("ClientId", UUID)
    >>> client_id_factory = LastUUIDFactory[ClientId](ClientId)
    >>> client_id_factory()
    UUID('019c21f2-43d6-7a1c-811e-5138f110345c')
    >>> client_id_factory()
    UUID('019c21f2-521f-7780-91e4-5a036d46e099')
    >>> client_id_factory()
    UUID('019c21f2-56a3-75e9-bac5-7cecf73a698a')
    >>> client_id_factory.last()
    UUID('019c21f2-56a3-75e9-bac5-7cecf73a698a')
    >>> client_id_factory.last(1)
    UUID('019c21f2-56a3-75e9-bac5-7cecf73a698a')
    >>> client_id_factory.last(2)
    UUID('019c21f2-521f-7780-91e4-5a036d46e099')
    >>> client_id_factory.last(3)
    UUID('019c21f2-43d6-7a1c-811e-5138f110345c')
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

    def last(self, i: int = 1) -> T:
        """Most recently generated UUID-NewType instance."""
        return self._cache[-i]
