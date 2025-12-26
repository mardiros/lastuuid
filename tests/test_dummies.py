from uuid import UUID

from lastuuid.dummies import uuid7gen, uuidgen


def test_default():
    assert uuidgen() == UUID(int=1)  # XXX this tests works because it is the first
    assert uuidgen.last == UUID(int=1)


def test_predictable():
    assert uuidgen(1) == UUID("00000001-0000-0000-0000-000000000000")
    assert uuidgen(1, 2, 3, 4, 5) == UUID("00000001-0002-0003-0004-000000000005")


def test_predictable_uuid7():
    myid = uuid7gen()
    assert myid == uuid7gen.last
