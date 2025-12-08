from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID, uuid4

import hashlib, json
from json import JSONEncoder

from fastapi import Header
from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional
from fastapi.responses import Response

from models.theatre import TheatreCreate, TheatreRead, TheatreUpdate
from models.screen import ScreenCreate, ScreenRead, ScreenUpdate
from models.cinema import CinemaCreate, CinemaRead, CinemaUpdate
from models.health import Health
from models.theatreDataService import TheatreDataService

port = int(os.environ.get("FASTAPIPORT", 5002))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
theatres: Dict[UUID, TheatreRead] = {}
screens: Dict[UUID, ScreenRead] = {}
cinemas: Dict[UUID, CinemaRead] = {}

app = FastAPI(
    title="Nebula Booking Theatre Service API",
    description="FastAPI app using Pydantic v2 models for Theatre, Screen, and Cinema management",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

class PydanticJSONEncoder(JSONEncoder):
    """Custom JSON encoder for Pydantic models with datetime and UUID support."""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)

def _calc_etag(obj) -> str:
    """
    Strong ETag: SHA-256 of the JSON payload (stable keys, no spaces).
    Returns a quoted value like "c0ffee...".
    """
    payload = json.dumps(
        obj.model_dump(exclude_none=True),
        sort_keys=True,
        separators=(",", ":"),
        cls=PydanticJSONEncoder,
    ).encode("utf-8")
    return f"\"{hashlib.sha256(payload).hexdigest()}\""

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Favicon (avoid noisy 404s from browsers)
# -----------------------------------------------------------------------------
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# -----------------------------------------------------------------------------
# Theatre endpoints
# -----------------------------------------------------------------------------

@app.post("/theatres", response_model=TheatreRead, status_code=201)
def create_theatre(theatre: TheatreCreate, response: Response):
    """Create a new theatre using the Theatre models."""
    new_theatre = TheatreRead(**theatre.model_dump())
    # store by the model's theatre_id
    theatres[new_theatre.theatre_id] = new_theatre
    response.headers["ETag"] = _calc_etag(new_theatre)
    return new_theatre

def _int_to_uuid(value: int) -> UUID:
    """Convert an integer ID to a UUID by padding to 32 hex characters."""
    if value is None:
        return uuid4()
    # Convert int to hex string, pad to 32 chars, then create UUID
    hex_str = f"{value:032x}"
    return UUID(hex_str)

@app.get("/theatres", response_model=List[TheatreRead])
def list_theatres(
    name: Optional[str] = Query(None, description="Filter by theatre name"),
    cinema_id: Optional[UUID] = Query(None, description="Filter by cinema_id"),
):
    """List theatres from the database using TheatreDataService. Supports filtering by name and cinema_id."""
    # Get theatres from database via TheatreDataService
    db_theatres = TheatreDataService().get_all_theatres()
    
    # Convert database results to TheatreRead objects
    items: List[TheatreRead] = []
    for db_item in db_theatres:
        # Database returns INT UNSIGNED for IDs, but model expects UUID
        # Database uses snake_case (screen_count), model uses camelCase (screenCount)
        theatre_id_val = db_item.get('theatre_id')
        cinema_id_val = db_item.get('cinema_id')
        
        # Handle created_at and updated_at - they might be datetime objects or strings
        created_at_val = db_item.get('created_at')
        if isinstance(created_at_val, datetime):
            created_at = created_at_val
        elif created_at_val:
            # Try parsing as ISO format
            if isinstance(created_at_val, str):
                created_at = datetime.fromisoformat(created_at_val.replace('Z', '+00:00'))
            else:
                created_at = datetime.utcnow()
        else:
            created_at = datetime.utcnow()
            
        updated_at_val = db_item.get('updated_at')
        if isinstance(updated_at_val, datetime):
            updated_at = updated_at_val
        elif updated_at_val:
            if isinstance(updated_at_val, str):
                updated_at = datetime.fromisoformat(updated_at_val.replace('Z', '+00:00'))
            else:
                updated_at = datetime.utcnow()
        else:
            updated_at = datetime.utcnow()
        
        theatre = TheatreRead(
            theatre_id=_int_to_uuid(theatre_id_val) if isinstance(theatre_id_val, int) else (UUID(str(theatre_id_val)) if theatre_id_val else uuid4()),
            name=db_item.get('name', ''),
            address=db_item.get('address', ''),
            cinema_id=_int_to_uuid(cinema_id_val) if isinstance(cinema_id_val, int) else (UUID(str(cinema_id_val)) if cinema_id_val else uuid4()),
            screenCount=db_item.get('screen_count', db_item.get('screenCount', 0)),
            created_at=created_at,
            updated_at=updated_at,
        )
        items.append(theatre)
    
    # Apply filters
    if name:
        items = [t for t in items if name.lower() in t.name.lower()]
    if cinema_id:
        items = [t for t in items if t.cinema_id == cinema_id]

    return items

@app.get("/theatres/{theatre_id}", response_model=TheatreRead)
def get_theatre(
    theatre_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None)  # maps to "If-None-Match"
):
    item = theatres.get(theatre_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Theatre not found")

    etag = _calc_etag(item)
    # If client's cached version matches, say "Not Modified"
    if if_none_match == etag:
        # Best practice: still echo current ETag in 304
        return Response(status_code=304, headers={"ETag": etag})

    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "private, max-age=60"
    
    return item

@app.patch("/theatres/{theatre_id}", response_model=TheatreRead)
def update_theatre(
    theatre_id: UUID,
    update: TheatreUpdate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    """Update a theatre (partial update)."""
    existing = theatres.get(theatre_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Theatre not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Merge updates onto existing model
    updates = update.model_dump(exclude_none=True)
    updated = existing.model_copy(update=updates)
    # Update the updated_at timestamp
    updated.updated_at = datetime.utcnow()
    theatres[theatre_id] = updated

    new_etag = _calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated

@app.put("/theatres/{theatre_id}", response_model=TheatreRead)
def replace_theatre(
    theatre_id: UUID,
    theatre: TheatreCreate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    existing = theatres.get(theatre_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Theatre not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Replace entire resource; keep the same id; update timestamps if your model has them
    replacement = TheatreRead(theatre_id=theatre_id, **theatre.model_dump())
    replacement.created_at = existing.created_at
    replacement.updated_at = existing.updated_at
    theatres[theatre_id] = replacement

    new_etag = _calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement


@app.delete("/theatres/{theatre_id}")
def delete_theatre(
    theatre_id: UUID,
    if_match: Optional[str] = Header(None)
):
    existing = theatres.get(theatre_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Theatre not found")

    current_etag = _calc_etag(existing)
    # If you want protection: only delete if client proves it has the latest
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    del theatres[theatre_id]
    return {"status": "deleted", "id": str(theatre_id)}


# -----------------------------------------------------------------------------
# Screen endpoints
# -----------------------------------------------------------------------------

@app.post("/screens", response_model=ScreenRead, status_code=201)
def create_screen(screen: ScreenCreate, response: Response):
    """Create a new screen and store it in the in-memory store."""
    new_screen = ScreenRead(**screen.model_dump())
    screens[new_screen.screen_id] = new_screen
    response.headers["ETag"] = _calc_etag(new_screen)
    return new_screen

@app.get("/screens", response_model=List[ScreenRead])
def list_screens(
    theatre_id: Optional[UUID] = Query(None, description="Filter by theatre ID"),
    screen_number: Optional[int] = Query(None, description="Filter by screen number"),
):
    """List all screens with optional filtering by theatre_id and screen_number."""
    items: List[ScreenRead] = list(screens.values())
    if theatre_id:
        items = [s for s in items if s.theatre_id == theatre_id]
    if screen_number is not None:
        items = [s for s in items if s.screen_number == screen_number]
    return items

@app.get("/screens/{screen_id}", response_model=ScreenRead)
def get_screen(
    screen_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None)  # maps to "If-None-Match"
):
    """Get a specific screen by ID."""
    item = screens.get(screen_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Screen not found")

    etag = _calc_etag(item)
    # If client's cached version matches, say "Not Modified"
    if if_none_match == etag:
        # Best practice: still echo current ETag in 304
        return Response(status_code=304, headers={"ETag": etag})

    response.headers["ETag"] = etag
    return item

@app.patch("/screens/{screen_id}", response_model=ScreenRead)
def update_screen(
    screen_id: UUID,
    update: ScreenUpdate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    """Update a screen (partial update)."""
    existing = screens.get(screen_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Screen not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Merge updates onto existing model
    updates = update.model_dump(exclude_none=True)
    updated = existing.model_copy(update=updates)
    # Update the updated_at timestamp
    updated.updated_at = datetime.utcnow()
    screens[screen_id] = updated

    new_etag = _calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated

@app.put("/screens/{screen_id}", response_model=ScreenRead)
def replace_screen(
    screen_id: UUID,
    screen: ScreenCreate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    """Replace entire screen resource (PUT - complete replacement)."""
    existing = screens.get(screen_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Screen not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Replace entire resource; keep the same id; update timestamps if your model has them
    replacement = ScreenRead(screen_id=screen_id, **screen.model_dump())
    # Update the updated_at timestamp
    replacement.updated_at = datetime.utcnow()
    screens[screen_id] = replacement

    new_etag = _calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement

@app.delete("/screens/{screen_id}")
def delete_screen(
    screen_id: UUID,
    if_match: Optional[str] = Header(None)
):
    """Delete a screen resource."""
    existing = screens.get(screen_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Screen not found")

    current_etag = _calc_etag(existing)
    # If you want protection: only delete if client proves it has the latest
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    del screens[screen_id]
    return {"status": "deleted", "id": str(screen_id)}

# -----------------------------------------------------------------------------
# Cinema endpoints
# -----------------------------------------------------------------------------

@app.post("/cinemas", response_model=CinemaRead, status_code=201)
def create_cinema(cinema: CinemaCreate, response: Response):
    """Create a new cinema using the Cinema models."""
    new_cinema = CinemaRead(**cinema.model_dump())
    # store by the model's cinema_id
    cinemas[new_cinema.cinema_id] = new_cinema
    response.headers["ETag"] = _calc_etag(new_cinema)
    return new_cinema

@app.get("/cinemas", response_model=List[CinemaRead])
def list_cinemas(
    name: Optional[str] = Query(None, description="Filter by cinema name"),
):
    """List cinemas from the in-memory store. Supports filtering by name."""
    items: List[CinemaRead] = list(cinemas.values())
    if name:
        items = [c for c in items if name.lower() in c.name.lower()]

    return items

@app.get("/cinemas/{cinema_id}", response_model=CinemaRead)
def get_cinema(
    cinema_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None)  # maps to "If-None-Match"
):
    item = cinemas.get(cinema_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Cinema not found")

    etag = _calc_etag(item)
    # If client's cached version matches, say "Not Modified"
    if if_none_match == etag:
        # Best practice: still echo current ETag in 304
        return Response(status_code=304, headers={"ETag": etag})

    response.headers["ETag"] = etag
    return item

@app.patch("/cinemas/{cinema_id}", response_model=CinemaRead)
def update_cinema(
    cinema_id: UUID,
    update: CinemaUpdate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    """Update a cinema (partial update)."""
    existing = cinemas.get(cinema_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Cinema not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Merge updates onto existing model
    updates = update.model_dump(exclude_none=True)
    updated = existing.model_copy(update=updates)
    # Update the updated_at timestamp
    updated.updated_at = datetime.utcnow()
    cinemas[cinema_id] = updated

    new_etag = _calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated

@app.put("/cinemas/{cinema_id}", response_model=CinemaRead)
def replace_cinema(
    cinema_id: UUID,
    cinema: CinemaCreate,
    response: Response,
    if_match: Optional[str] = Header(None)  # maps to "If-Match"
):
    existing = cinemas.get(cinema_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Cinema not found")

    current_etag = _calc_etag(existing)

    # Enforce optimistic concurrency: require If-Match and it must match
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    # Replace entire resource; keep the same id; update timestamps if your model has them
    replacement = CinemaRead(cinema_id=cinema_id, **cinema.model_dump())
    # Update the updated_at timestamp
    replacement.updated_at = datetime.utcnow()
    cinemas[cinema_id] = replacement

    new_etag = _calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement

@app.delete("/cinemas/{cinema_id}")
def delete_cinema(
    cinema_id: UUID,
    if_match: Optional[str] = Header(None)
):
    existing = cinemas.get(cinema_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Cinema not found")

    current_etag = _calc_etag(existing)
    # If you want protection: only delete if client proves it has the latest
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")

    del cinemas[cinema_id]
    return {"status": "deleted", "id": str(cinema_id)}

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Nebula Booking Theatre Service API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)