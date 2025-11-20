"""Health check API endpoints."""

import socket
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Path, Query
from fastapi.responses import Response

from schemas.health import Health


router = APIRouter(prefix="/health", tags=["health"])


def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    """
    Create a Health response object.

    Args:
        echo: Optional echo string from query parameter
        path_echo: Optional echo string from path parameter

    Returns:
        Health: Health check response object
    """
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )


@router.get("", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    """Health check endpoint without path parameter."""
    return make_health(echo=echo, path_echo=None)


@router.get("/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    """Health check endpoint with path parameter."""
    return make_health(echo=echo, path_echo=path_echo)


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Favicon endpoint to avoid noisy 404s from browsers."""
    return Response(status_code=204)
