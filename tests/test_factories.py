from typing import NewType, assert_type
from uuid import UUID

from lastuuid.factories import (
    LastUUIDFactory,
    NewTypeFactory,
)


def test_newtype_factory():
    UserId = NewType("UserId", UUID)
    newtype = NewTypeFactory[UserId](UserId)
    val = newtype()
    assert_type(val, UserId)


def test_last_uuid_factory():
    ClientId = NewType("ClientId", UUID)

    client_id_factory = LastUUIDFactory[ClientId](ClientId, cache_size=2)
    myid = client_id_factory()
    assert myid == client_id_factory.last
    myid2 = client_id_factory()
    assert myid2 == client_id_factory.last
    assert [myid2, myid] == client_id_factory.lasts
    myid3 = client_id_factory()
    assert myid3 == client_id_factory.last
    assert [myid3, myid2] == client_id_factory.lasts
