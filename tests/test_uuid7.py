from uuid import UUID
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import BaseModel, Field

from lastuuid import uuid7, uuid7_to_datetime


dummy_timezone = timezone(timedelta(hours=2))


class Dummy(BaseModel):
    id: UUID = Field(default_factory=uuid7)


def test_dummy():
    dummy = Dummy()
    dummy2 = Dummy()
    assert dummy.id.bytes < dummy2.id.bytes

    assert dummy.model_dump(mode="json") == {"id": str(dummy.id)}


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
