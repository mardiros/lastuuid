from uuid import UUID
from pydantic import BaseModel, Field

from lastuuid import uuid7


class Dummy(BaseModel):
    id: UUID = Field(default_factory=uuid7)


def test_dummy():
    dummy = Dummy()
    dummy2 = Dummy()
    assert dummy.id.bytes < dummy2.id.bytes

    assert dummy.model_dump(mode="json") == {"id": str(dummy.id)}
