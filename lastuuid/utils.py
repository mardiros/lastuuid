from datetime import date, datetime
from typing_extensions import Tuple
from uuid import UUID


def datetime_to_uuid7_low(dt: datetime) -> UUID:
    # Convert datetime to Unix timestamp in milliseconds
    unix_ts_ms = int(dt.timestamp() * 1000)
    version = 0x07
    var = 2
    final_bytes = unix_ts_ms.to_bytes(6)
    final_bytes += (version << 12).to_bytes(2)
    final_bytes += ((var << 62) + 0x3000000000000000).to_bytes(8)
    return UUID(bytes=final_bytes)


def datetime_to_uuid7_high(dt: datetime) -> UUID:
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
    return datetime_to_uuid7_low(dtlow), datetime_to_uuid7_high(dthigh or dtlow)
