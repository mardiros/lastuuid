# lastuuid - yet another uuid library

[![Documentation](https://github.com/mardiros/lastuuid/actions/workflows/publish-doc.yml/badge.svg)](https://mardiros.github.io/lastuuid/)
[![Continuous Integration](https://github.com/mardiros/lastuuid/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/lastuuid/actions/workflows/tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/8e7293fabe7508b2ec6c/maintainability)](https://codeclimate.com/github/mardiros/lastuuid/maintainability)

UUID type is awesome, but, at the moment, the UUID type in the standard library
does not support the uuid7 format.

You may find plenty of library that implement uuid7, but they have downside,
such has ignoring pull request to fix issues, or not compatible with Pydantic.

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

### Read More

There are other usefull function in the library that cab be found in the
[API documentation](https://mardiros.github.io/lastuuid/).

https://mardiros.github.io/lastuuid/
