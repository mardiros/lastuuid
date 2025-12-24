"""
A dummy uuid usefull for unit testing purpose.

UUID generated here are full of 0, they does not respect any kind of UUID version,
they remove a bit of cognitive load while testing.
"""

from collections import deque
from typing import (
    Any,
    Deque,
    Generic,
    Iterator,
    List,
    TypeVar,
)
from uuid import UUID

from lastuuid import uuid7

__all__ = ["uuidgen", "uuid7gen", "LastUUID7Factory"]


def gen_id() -> Iterator[int]:
    num = 0
    while True:
        num += 1
        yield num


next_id = gen_id()


def uuidgen(i: int = 0, j: int = 0, k: int = 0, x: int = 0, y: int = 0) -> UUID:
    """
    A UUID generator that makes UUIDs more readable for humans.

    # Generate autoincrement UUID that you need to predict

    Sometime you prepare fixtures with well known UUID and you want to repeat them,

    uuidgen(1) is more readable that UUID('00000001-0000-0000-0000-000000000000'),
    this is why this function is made for.
    Every section of the uuid can be filled out using `i`, `j`, `k`, `x`, `y` but,
    I personnaly never use more than `i` and `j`.

    ```python
    >>> from lastuuid.dummies import uuidgen
    >>> uuidgen(1)
    UUID('00000001-0000-0000-0000-000000000000')
    >>> uuidgen(1, 2)
    UUID('00000001-0002-0000-0000-000000000000')
    >>> uuidgen(1, 2, 3, 4, 5)
    UUID('00000001-0002-0003-0004-000000000005')
    ```

    ```{tip}
    if you don't want a dependency for that, the standard library let you write
    UUID(int=1) which produce UUID('00000000-0000-0000-0000-000000000001').
    ```

    # Generate autoincrement UUID that you don't need to predict

    Without any parameter, it will generate UUID where the last bits are incremented.

    ```python
    >>> from lastuuid.dummies import uuidgen
    >>> uuidgen()
    UUID('00000000-0000-0000-0000-000000000001')
    >>> uuidgen()
    UUID('00000000-0000-0000-0000-000000000002')
    ```

    """
    if i == 0 and y == 0:
        y = next(next_id)
    return UUID(f"{i:0>8}-{j:0>4}-{k:0>4}-{x:0>4}-{y:0>12}")


T = TypeVar("T", bound=UUID)


class LastUUID7Factory(Generic[T]):
    """
    Factory for NewType UUIDs with last N cache.

    ```python
    >>> from typing import NewType
    >>> from uuid import UUID
    >>> from lastuuid.dummies import LastUUID7Factory
    >>> ClientId = NewType("ClientId", UUID)
    >>> client_id_factory = LastUUID7Factory[ClientId](ClientId)
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

    def __init__(self, newtype: Any, cache_size: int = 24):
        """
        Create a factory of type that store the last instances.

        :param newtype: the type to be used
        :param cache_size: size of the queue that saved the last uuids
        """
        self._newtype = newtype
        self._cache: Deque[T] = deque(maxlen=cache_size)

    def __call__(self) -> T:
        val = uuid7()
        if self._newtype:
            val: T = self._newtype(val)  # cast to NewType
        self._cache.append(val)
        return val

    @property
    def last(self) -> T:
        """Most recently generated UUID-NewType instance."""
        return self._cache[-1]

    @property
    def lasts(self) -> List[T]:
        """
        Returns a list of the last N generated UUID-NewType instances.

        The list is ordered from most recent to oldest.
        The most recent value is accessible via `last`.
        """
        return list(reversed(self._cache))


uuid7gen = LastUUID7Factory(None)
