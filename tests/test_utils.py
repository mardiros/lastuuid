from uuid import UUID
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from lastuuid import uuid7_to_datetime

dummy_timezone = timezone(timedelta(hours=2))


def test_uuid7_to_datetime_default():
    assert uuid7_to_datetime(UUID("019500d0-468f-7eaa-ab66-f90e998cd72c")) == datetime(
        2025, 2, 13, 19, 36, 44, 431000, tzinfo=timezone.utc
    )


def test_uuid7_to_datetime_naive_custom_timezone():
    assert uuid7_to_datetime(
        UUID("019500d0-468f-7eaa-ab66-f90e998cd72c"), tz=dummy_timezone
    ) == datetime(2025, 2, 13, 21, 36, 44, 431000, tzinfo=dummy_timezone)


def test_uuid7_to_datetime_uuid4():
    with pytest.raises(ValueError) as ctx:
        uuid7_to_datetime(UUID("2e92c8da-0b38-4d95-a627-d6e761f764f9"))
    assert str(ctx.value) == "UUIDv7 expected, received UUIDv4"
