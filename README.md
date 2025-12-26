# lastuuid - yet another uuid library

[![Documentation](https://github.com/mardiros/lastuuid/actions/workflows/publish-doc.yml/badge.svg)](https://mardiros.github.io/lastuuid/)
[![Continuous Integration](https://github.com/mardiros/lastuuid/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/lastuuid/actions/workflows/tests.yml)

UUID type is awesome, but, at the moment, the UUID type in the standard library
does not support the uuid7 format.

**lastuuid** provide **fast UUIDv7 generation** made by the
[rust crate uuid7](https://crates.io/crates/uuid7) **compatible with Pydantic**.

It has additional features that may helps for testing or inspecting UUIDv7.

```{note}
lastuuid is a developer joke based on the nature of UUIDv7,

where the most recently generated UUID is always the last one when sorted.
```

## Usage

### UUID7

```python
>>> from lastuuid import uuid7
>>> uuid7()
UUID('019316cc-f99a-77b3-89d5-ed8c3cf1f50e')
```

There is no parameter here, the uuid is generated from the current time.

The implementation of uuid7 algorithm is made in the uuid7 rust crate.

#### Pydantic

This lib has been created because all the other library that implement uuid7
create there own UUID type, so its not easy to use with pydantic.

```python
from uuid import UUID
from pydantic import BaseModel, Field

from lastuuid import uuid7


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid7)

```

#### NewType


The NewTypeFactory will generate an uuid7 for a new defined type.

```python
from typing import NewType

from uuid import UUID
from pydantic import BaseModel, Field

from lastuuid.utils import NewTypeFactory


MessageID = NewType("MessageID", UUID)
message_id = NewTypeFactory[MessageID](MessageID)


class Message(BaseModel):
    id: UUID = Field(default_factory=message_id)

```

The message_id here will generate a uuid7 typed MessageID,

this avoid to write `MessageID(uuid7())` to have a MessageID typed uuid.


#### Performance

On my machine the uuid7 is as fast (or slow) as the native uuid4.

```bash
$ python -m timeit "from lastuuid import uuid7; uuid7()"
200000 loops, best of 5: 1.8 usec per loop

$ python -m timeit "from uuid import uuid4; uuid4()"
200000 loops, best of 5: 1.82 usec per loop
```

### Read More

There are other usefull function in the library that cab be found in the
[API documentation](https://mardiros.github.io/lastuuid/).

https://mardiros.github.io/lastuuid/
