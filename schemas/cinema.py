from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
class CinemaBase(BaseModel):
    name: str = Field(
        ...,
        description="Cinema name.",
        json_schema_extra={"example": "Cineplex 20"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Cineplex 20",
                }
            ]
        }
    }   
class CinemaCreate(CinemaBase):
    """Creation payload for a Cinema."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Grand Cinema",
                }
            ]
        }
    }
class CinemaUpdate(BaseModel):
    """Partial update for a Cinema; supply only fields to change."""
    name: Optional[str] = Field(None, description="Cinema name")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Cineplex 25 Updated"},
            ]
        }
    }
class CinemaRead(CinemaBase):
    """Server representation returned to clients."""
    cinema_id: int = Field(
        ...,
        description="Server-generated Cinema ID.",
        json_schema_extra={"example": 301},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cinema_id": "1",
                    "name": "Cineplex 20",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }

