from datetime import UTC, date, datetime
from uuid import UUID

from lastuuid.utils import (
    uuid7_bounds_from_date,
    uuid7_bounds_from_datetime,
)


def test_uuid7_range_from_datetime():
    dt = datetime(2025, 2, 14, 0, 0, 0, tzinfo=UTC)
    left, right = uuid7_bounds_from_datetime(dt)
    assert left == UUID("019501c1-4c00-7000-b000-000000000000")
    assert right == UUID("019501c1-4c01-7000-b000-000000000000")


def test_uuid7_range_from_datetime_2():
    dt1 = datetime(2025, 2, 14, 0, 0, 0, tzinfo=UTC)
    dt2 = datetime(2025, 2, 15, 0, 0, 0, tzinfo=UTC)
    left, right = uuid7_bounds_from_datetime(dt1, dt2)
    assert left == UUID("019501c1-4c00-7000-b000-000000000000")
    assert right == UUID("019506e7-a800-7000-b000-000000000000")


def test_uuid7_range_from_date():
    dt1 = date(2025, 2, 14)
    left, right = uuid7_bounds_from_date(dt1)
    assert left == UUID("019501c1-4c00-7000-b000-000000000000")
    assert right == UUID("019506e7-a800-7000-b000-000000000000")
