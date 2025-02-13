from uuid import UUID
from datetime import datetime, timezone

from lastuuid import uuid7_to_datetime


def test_uuid7_to_datetime():
    assert uuid7_to_datetime(UUID("019500d0-468f-7eaa-ab66-f90e998cd72c")) == datetime(
        2025, 2, 13, 19, 36, 44, 431000, tzinfo=timezone.utc
    )
