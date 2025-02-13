from uuid import UUID
from datetime import datetime, timezone


def uuid7_to_datetime(uuid7: UUID, tz=timezone.utc) -> datetime:
    """Extract the datetime part of an uuid 7."""
    # Extract the first 6 bytes (48 bits) and interpret as a big-endian integer (milliseconds)
    ms_since_epoch = int.from_bytes(uuid7.bytes[:6], byteorder="big")
    # Convert milliseconds to seconds and create a datetime object (UTC)
    return datetime.fromtimestamp(ms_since_epoch / 1000, tz=tz)
