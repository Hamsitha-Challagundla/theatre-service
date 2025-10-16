from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class TheatreBase(BaseModel):
    name: str = Field(
        ...,
        description="Theatre name.",
        json_schema_extra={"example": "AMC Times Square"},
    )
    address: str = Field(
        ...,
        description="Theatre address.",
        json_schema_extra={"example": "234 W 42nd St, New York, NY 10036"},
    )
    city: str = Field(
        ...,
        description="City where the theatre is located.",
        json_schema_extra={"example": "New York"},
    )
    state: str = Field(
        ...,
        description="State or province where the theatre is located.",
        json_schema_extra={"example": "NY"},
    )
    postal_code: str = Field(
        ...,
        description="Postal code of the theatre.",
        json_schema_extra={"example": "10036"},
    )
    country: str = Field(
        ...,
        description="Country where the theatre is located.",
        json_schema_extra={"example": "USA"},
    )
    phone: Optional[str] = Field(
        None,
        description="Theatre contact phone number.",
        json_schema_extra={"example": "+1-212-555-0123"},
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Theatre contact email.",
        json_schema_extra={"example": "info@amctimesquare.com"},
    )
    capacity: Optional[int] = Field(
        None,
        description="Total seating capacity of the theatre.",
        json_schema_extra={"example": 500},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "AMC Times Square",
                    "address": "234 W 42nd St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10036",
                    "country": "USA",
                    "phone": "+1-212-555-0123",
                    "email": "info@amctimesquare.com",
                    "capacity": 500,
                }
            ]
        }
    }


class TheatreCreate(TheatreBase):
    """Creation payload for a Theatre."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Regal Union Square",
                    "address": "850 Broadway",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10003",
                    "country": "USA",
                    "phone": "+1-212-555-0456",
                    "email": "info@regalunionsquare.com",
                    "capacity": 300,
                }
            ]
        }
    }


class TheatreUpdate(BaseModel):
    """Partial update for a Theatre; supply only fields to change."""
    name: Optional[str] = Field(None, description="Theatre name")
    address: Optional[str] = Field(None, description="Theatre address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: Optional[str] = Field(None, description="Postal code")
    country: Optional[str] = Field(None, description="Country")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    capacity: Optional[int] = Field(None, description="Total seating capacity")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "AMC Times Square Updated"},
                {"phone": "+1-212-555-0789"},
                {"capacity": 600},
            ]
        }
    }


class TheatreRead(TheatreBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Theatre ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "name": "AMC Times Square",
                    "address": "234 W 42nd St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10036",
                    "country": "USA",
                    "phone": "+1-212-555-0123",
                    "email": "info@amctimesquare.com",
                    "capacity": 500,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
