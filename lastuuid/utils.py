"""
Utilities methods that may be used for database querying purpose.

Because UUIDv7 are timestamped ordered and monotonically increasing,
there are a good solution for generating primary keys.

The design of UUIDv7 feet well with the design of BTree.

Because they contains a date time, a UUID range can be compute
in order to retrieve UUIDs generated at a given time.


```{important}
In a distributed system, relying solely on a datetime or UUIDv7 for sorting
has limitations.
While UUIDv7 ensures sequential ordering on a single machine, there is no guarantee
that a UUIDv7 generated later on one machine will be greater than one generated
earlier on another machine.

This documentation does not cover the book Designing Data-Intensive Applications ;).
```
"""

from collections import deque
from collections.abc import Callable
from datetime import UTC, date, datetime, time, timedelta
from typing import Any, Deque, Generic, TypeVar
from uuid import UUID

from .lastuuid import uuid7

__all__ = [
    "uuid7_bounds_from_datetime",
    "uuid7_bounds_from_date",
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
        val = self._id_factory(*args, **kwargs)  # type: ignore
        if self._newtype:
            val: T = self._newtype(val)  # cast to NewType
        return val


class LastUUIDFactory(NewTypeFactory[T]):
    def __init__(
        self,
        newtype: Any,
        id_factory: Callable[[], UUID] = uuid7,
        cache_size: int = 10,
    ):
        """
        Create a factory of type that store the last instances.

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

        :param newtype: the type to be used
        :param cache_size: size of the queue that saved the last uuids
        """
        super().__init__(newtype, id_factory)
        self._cache: Deque[T] = deque(maxlen=cache_size)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
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


def _datetime_to_uuid7_lowest(dt: datetime) -> UUID:
    unix_ts_ms = int(dt.timestamp() * 1000)
    version = 0x07
    var = 2
    final_bytes = unix_ts_ms.to_bytes(6)
    final_bytes += (version << 12).to_bytes(2)
    final_bytes += ((var << 62) + 0x3000000000000000).to_bytes(8)
    return UUID(bytes=final_bytes)


def uuid7_bounds_from_datetime(
    dt_lower: datetime,
    dt_upper: datetime | None = None,
) -> tuple[UUID, UUID]:
    """
    Get uuid bound for a half-open interval.

    This function can be usefull to search for any rows based on a uuid7 in a sql query.
    If one parameter is set, then the search is based on a millisecond, because uuid7
    are only millisecond precision.

    The returned bound are half open, so the upper bound, from the ``dt_upper`` will
    not include in the result, only the first value to be excluded.

    If the the second parameter is ommited, then the bound only contains a millisecond,
    of dt_lower.

    :param dt_lower: the included left bound of the range.
    :param dt_upper: the excluded right bound of the range.
    """
    return _datetime_to_uuid7_lowest(dt_lower), _datetime_to_uuid7_lowest(
        dt_upper or (dt_lower + timedelta(milliseconds=1))
    )


def uuid7_bounds_from_date(dt: date, tz=UTC) -> tuple[UUID, UUID]:
    """
    Get uuid bound for a particular day.

    This function can be usefull to search for any rows based on a uuid7 in a sql query.
    The right bound return is the first uuid of the next day that should be excluded.

    :param dt: the included left bound of the range.
    :param tz: the timezone used to compute the UUID, it should always be ommited.
    """
    return _datetime_to_uuid7_lowest(
        datetime.combine(dt, time=time(tzinfo=tz))
    ), _datetime_to_uuid7_lowest(
        datetime.combine(dt + timedelta(days=1), time=time(tzinfo=tz))
    )
