"""Pyo3 binding interface definition."""

from uuid import UUID


def uuid7() -> UUID:
    """
    Generate an uuid using uuidv7 format, the best format that feet in a BTree.
    """
