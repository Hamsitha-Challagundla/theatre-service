"""Theatre API endpoints - using SQLAlchemy ORM."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Header, Query, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from schemas.theatre import TheatreCreate, TheatreRead, TheatreUpdate
from services.theatreDataService import TheatreDataService
from database import get_db
from utils.etag import calc_etag
from utils.converters import dict_to_theatre_read, db_to_uuid


router = APIRouter(prefix="/theatres", tags=["theatres"])
service = TheatreDataService()


@router.post("", response_model=TheatreRead, status_code=201)
def create_theatre(
    theatre: TheatreCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """Create a new theatre in the database."""
    new_theatre = service.create_theatre(
        db=db,
        cinema_id=1,  # Placeholder - would map UUID to int
        name=theatre.name,
        address=theatre.address,
        screen_count=theatre.screenCount,
        created_by=1  # Placeholder - would come from auth
    )
    
    theatre_read = TheatreRead(**dict_to_theatre_read(new_theatre))
    response.headers["ETag"] = calc_etag(theatre_read)
    return theatre_read


@router.get("", response_model=List[TheatreRead])
def list_theatres(
    name: Optional[str] = Query(None, description="Filter by theatre name"),
    cinema_id: Optional[UUID] = Query(None, description="Filter by cinema_id"),
    db: Session = Depends(get_db)
):
    """List theatres from the database. Supports filtering by name and cinema_id."""
    theatres = service.get_all_theatres(db)
    
    items: List[TheatreRead] = [
        TheatreRead(**dict_to_theatre_read(t))
        for t in theatres
    ]
    
    # Apply filters
    if name:
        items = [t for t in items if name.lower() in t.name.lower()]
    if cinema_id:
        items = [t for t in items if t.cinema_id == cinema_id]
    
    return items


@router.get("/{theatre_id}", response_model=TheatreRead)
def get_theatre(
    theatre_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get a specific theatre from the database by ID."""
    theatre_id_int = int(str(theatre_id).replace('-', '')[:8], 16) % (10**9)
    
    theatre = service.get_theatre_by_id(db, theatre_id_int)
    if not theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    item = TheatreRead(**dict_to_theatre_read(theatre))
    etag = calc_etag(item)
    
    if if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})
    
    response.headers["ETag"] = etag
    return item


@router.patch("/{theatre_id}", response_model=TheatreRead)
def update_theatre(
    theatre_id: UUID,
    update: TheatreUpdate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Update a theatre (partial update) in the database."""
    theatre_id_int = int(str(theatre_id).replace('-', '')[:8], 16) % (10**9)
    
    theatre = service.get_theatre_by_id(db, theatre_id_int)
    if not theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    existing = TheatreRead(**dict_to_theatre_read(theatre))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    updates = update.model_dump(exclude_none=True)
    updated_theatre = service.update_theatre(
        db=db,
        theatre_id=theatre_id_int,
        name=updates.get('name'),
        address=updates.get('address'),
        screen_count=updates.get('screenCount')
    )
    
    if not updated_theatre:
        raise HTTPException(status_code=500, detail="Failed to update theatre")
    
    result = TheatreRead(**dict_to_theatre_read(updated_theatre))
    new_etag = calc_etag(result)
    response.headers["ETag"] = new_etag
    return result


@router.put("/{theatre_id}", response_model=TheatreRead)
def replace_theatre(
    theatre_id: UUID,
    theatre: TheatreCreate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Replace entire theatre resource (PUT) in the database."""
    theatre_id_int = int(str(theatre_id).replace('-', '')[:8], 16) % (10**9)
    
    existing_theatre = service.get_theatre_by_id(db, theatre_id_int)
    if not existing_theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    existing = TheatreRead(**dict_to_theatre_read(existing_theatre))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    updated_theatre = service.update_theatre(
        db=db,
        theatre_id=theatre_id_int,
        name=theatre.name,
        address=theatre.address,
        screen_count=theatre.screenCount
    )
    
    if not updated_theatre:
        raise HTTPException(status_code=500, detail="Failed to replace theatre")
    
    result = TheatreRead(**dict_to_theatre_read(updated_theatre))
    new_etag = calc_etag(result)
    response.headers["ETag"] = new_etag
    return result


@router.delete("/{theatre_id}")
def delete_theatre(
    theatre_id: UUID,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Soft delete a theatre from the database."""
    theatre_id_int = int(str(theatre_id).replace('-', '')[:8], 16) % (10**9)
    
    theatre = service.get_theatre_by_id(db, theatre_id_int)
    if not theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    
    existing = TheatreRead(**dict_to_theatre_read(theatre))
    current_etag = calc_etag(existing)
    
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = service.delete_theatre(db, theatre_id_int)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete theatre")
    
    return {"status": "deleted", "id": str(theatre_id)}
