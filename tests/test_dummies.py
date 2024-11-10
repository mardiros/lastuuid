from uuid import UUID
from lastuuid.dummies import uuidgen


def test_default():
    assert uuidgen() == UUID(int=1)


def test_predictable():
    assert uuidgen(1) == UUID("00000001-0000-0000-0000-000000000000")
    assert uuidgen(1, 2, 3, 4, 5) == UUID("00000001-0002-0003-0004-000000000005")
