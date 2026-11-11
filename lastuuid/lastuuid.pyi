"""Pyo3 binding interface definition."""

from datetime import datetime, timezone
from uuid import UUID

def uuid7() -> UUID:
    """
    Generate an uuid using uuidv7 format, the best format that feet in a BTree.
    """


def uuid7_to_datetime(uuid7: UUID, tz=timezone.utc) -> datetime:
    """Extract the datetime part of an uuid 7."""
