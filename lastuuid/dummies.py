"""A dummy uuid usefull for unit testing purpose."""

from typing import Iterator
from uuid import UUID


def gen_id() -> Iterator[int]:
    num = 0
    while True:
        num += 1
        yield num


next_id = gen_id()


def uuidgen(i: int = 0, j: int = 0, k: int = 0, x: int = 0, y: int = 0) -> UUID:
    """
    A UUID generator that makes UUIDs more readable for humans.
    """
    if i == 0 and y == 0:
        y = next(next_id)
    return UUID(f"{i:0>8}-{j:0>4}-{k:0>4}-{x:0>4}-{y:0>12}")
