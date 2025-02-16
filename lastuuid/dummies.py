"""
A dummy uuid usefull for unit testing purpose.

UUID generated here are full of 0, they does not respect any kind of UUID version,
they remove a bit of cognitive load while testing.
"""

from typing import Iterator
from uuid import UUID

__all__ = ["uuidgen"]


def gen_id() -> Iterator[int]:
    num = 0
    while True:
        num += 1
        yield num


next_id = gen_id()


def uuidgen(i: int = 0, j: int = 0, k: int = 0, x: int = 0, y: int = 0) -> UUID:
    """
    A UUID generator that makes UUIDs more readable for humans.

    # Generate autoincrement UUID that you need to predict

    Sometime you prepare fixtures with well known UUID and you want to repeat them,

    uuidgen(1) is more readable that UUID('00000001-0000-0000-0000-000000000000'),
    this is why this function is made for.
    Every section of the uuid can be filled out using `i`, `j`, `k`, `x`, `y` but,
    I personnaly never use more than `i` and `j`.

    ```python
    >>> from lastuuid.dummies import uuidgen
    >>> uuidgen(1)
    UUID('00000001-0000-0000-0000-000000000000')
    >>> uuidgen(1, 2)
    UUID('00000001-0002-0000-0000-000000000000')
    >>> uuidgen(1, 2, 3, 4, 5)
    UUID('00000001-0002-0003-0004-000000000005')
    ```

    ```{tip}
    if you don't want a dependency for that, the standard library let you write
    UUID(int=1) which produce UUID('00000000-0000-0000-0000-000000000001').
    ```

    # Generate autoincrement UUID that you don't need to predict

    Without any parameter, it will generate UUID where the last bits are incremented.

    ```python
    >>> from lastuuid.dummies import uuidgen
    >>> uuidgen()
    UUID('00000000-0000-0000-0000-000000000001')
    >>> uuidgen()
    UUID('00000000-0000-0000-0000-000000000002')
    ```

    """
    if i == 0 and y == 0:
        y = next(next_id)
    return UUID(f"{i:0>8}-{j:0>4}-{k:0>4}-{x:0>4}-{y:0>12}")
