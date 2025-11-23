"""Utility functions for ETag calculation."""

import hashlib
import json
from datetime import datetime
from json import JSONEncoder


class PydanticJSONEncoder(JSONEncoder):
    """Custom JSON encoder for Pydantic models with datetime support."""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
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
