"""Utility functions for ETag calculation and data type conversions."""

import hashlib
import json
from datetime import datetime
from json import JSONEncoder
from uuid import UUID, uuid4


class PydanticJSONEncoder(JSONEncoder):
    """Custom JSON encoder for Pydantic models with datetime and UUID support."""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


def calc_etag(obj) -> str:
    """
    Calculate a strong ETag: SHA-256 of the JSON payload (stable keys, no spaces).
    Returns a quoted value like "c0ffee...".

    Args:
        obj: Pydantic model instance to calculate ETag for

    Returns:
        str: Quoted SHA-256 hash of the serialized object
    """
    payload = json.dumps(
        obj.model_dump(exclude_none=True),
        sort_keys=True,
        separators=(",", ":"),
        cls=PydanticJSONEncoder,
    ).encode("utf-8")
    return f'"{hashlib.sha256(payload).hexdigest()}"'


def int_to_uuid(value: int) -> UUID:
    """
    Convert an integer ID to a UUID by padding to 32 hex characters.

    Args:
        value: Integer to convert to UUID

    Returns:
        UUID: Generated UUID from integer value, or random UUID if value is None
    """
    if value is None:
        return uuid4()
    # Convert int to hex string, pad to 32 chars, then create UUID
    hex_str = f"{value:032x}"
    return UUID(hex_str)
