"""
Utilities methods that may be used for database querying purpose.

Because UUIDv7 are timestamped ordered and monotonically increasing,
there are a good solution for generating primary keys.

The design of UUIDv7 feet well with the design of BTree.

Because they contains a date time, a UUID range can be compute
in order to retrieve UUIDs generated at a given time.

"""

from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID

__all__ = [
    "uuid7_bounds_from_datetime",
    "uuid7_bounds_from_date",
]


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
