"""Utilities method that may be used for database querying purpose."""

from datetime import UTC, date, datetime, time, timedelta
from typing_extensions import Tuple
from uuid import UUID


def _datetime_to_uuid7_low(dt: datetime) -> UUID:
    # Convert datetime to Unix timestamp in milliseconds
    unix_ts_ms = int(dt.timestamp() * 1000)
    version = 0x07
    var = 2
    final_bytes = unix_ts_ms.to_bytes(6)
    final_bytes += (version << 12).to_bytes(2)
    final_bytes += ((var << 62) + 0x3000000000000000).to_bytes(8)
    return UUID(bytes=final_bytes)


def _datetime_to_uuid7_high(dt: datetime) -> UUID:
    # Convert datetime to Unix timestamp in milliseconds
    unix_ts_ms = int(dt.timestamp() * 1000)
    version = 0x07
    var = 2
    final_bytes = unix_ts_ms.to_bytes(6)
    final_bytes += ((version << 12) + 0xFFF).to_bytes(2)
    final_bytes += ((var << 62) + 0x3FFFFFFFFFFFFFFF).to_bytes(8)
    return UUID(bytes=final_bytes)


def uuid7_bounds_from_datetime(
    dtlow: datetime,
    dthigh: datetime | None = None,
) -> Tuple[UUID, UUID]:
    """
    Get uuid bound for a particular datetime, or two.

    This function can be usefull to search for any rows based on a uuid7 in a sql query.
    If one parameter is set, then the search is based on a millisecond, because uuid7
    are millisecond.
    If two parameter are passed, the left range is from the first args (dtlow),
    and the right range is the second args (dtlow), note that those bounds
    are still millisecond.
    """
    return _datetime_to_uuid7_low(dtlow), _datetime_to_uuid7_high(dthigh or dtlow)


def uuid7_bounds_from_date(dt: date, tz=UTC) -> Tuple[UUID, UUID]:
    """
    Get uuid bound for a particular day.

    This function can be usefull to search for any rows based on a uuid7 in a sql query.
    The right bound return is the first uuid of the next day.
    """
    return _datetime_to_uuid7_low(
        datetime.combine(dt, time=time(tzinfo=tz))
    ), _datetime_to_uuid7_low(
        datetime.combine(dt + timedelta(days=1), time=time(tzinfo=tz))
    )
