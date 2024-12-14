# lastuuid - yet another uuid library

UUID type is awesome, but, at the moment, the UUID type in the standard library
does not support the uuid7 format.

This is where lastuuid library is usefull.

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


class Dummy(BaseModel):
    id: UUID = Field(default_factory=uuid7)

```

#### Performance

On my machine the uuid7 is as fast (or slow) as the native uuid4.

```bash
$ python -m timeit "from lastuuid import uuid7; uuid7()"
200000 loops, best of 5: 1.8 usec per loop

$ python -m timeit "from uuid import uuid4; uuid4()"
200000 loops, best of 5: 1.82 usec per loop
```

### Testing with uuid without a brain

The uuidgen method is not made for production code, it is not suited to be
fast, it is here to generate uuid has autoincrement or as redictable ids,
because UUID are made to create an identifier before it's saved into a
database.


Autoincrement your uuid in a test suite avoid some brain pain:

```python
>>> from lastuuid.dummies import uuidgen
>>> uuidgen()
UUID('00000000-0000-0000-0000-000000000001')
>>> uuidgen()
UUID('00000000-0000-0000-0000-000000000002')
```

Or even more usefull:

UUID predicted, where only the first bunch of bytes needs to be read; or a few,
to arrange some object ids.


```python
>>> from lastuuid.dummies import uuidgen
>>> uuidgen(1)
UUID('00000001-0000-0000-0000-000000000000')
>>> uuidgen(1, 2, 3, 4, 5)
UUID('00000001-0002-0003-0004-000000000005')
```
