"""Cinema API endpoints - connected to database."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Header, Query, Depends
from fastapi.responses import Response

from schemas.cinema import CinemaCreate, CinemaRead, CinemaUpdate
from services.cinemaDataService import CinemaDataService
from utils.etag import calc_etag
from utils.converters import dict_to_cinema_read
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/cinemas", tags=["cinemas"])


@router.post("", response_model=CinemaRead, status_code=201)
def create_cinema(cinema: CinemaCreate, response: Response, db: Session = Depends(get_db)):
    """Create a new cinema in the database."""
    db_service = CinemaDataService()
    
    cinema_id = db_service.create_cinema(
        db=db,
        name=cinema.name,
        created_by=1  # Placeholder - would come from auth
    )
    
    db_item = db_service.get_cinema_by_id(cinema_id) # why is this get cinema call needed while creating cinema?
    if not db_item:
        raise HTTPException(status_code=500, detail="Failed to create cinema")
    
    new_cinema = CinemaRead(**dict_to_cinema_read(db_item))
    response.headers["ETag"] = calc_etag(new_cinema)
    return new_cinema


@router.get("", response_model=List[CinemaRead])
def list_cinemas(
    name: Optional[str] = Query(None, description="Filter by cinema name"),
    db: Session = Depends(get_db),
):
    """List cinemas from the database. Supports filtering by name."""
    db_service = CinemaDataService()
    db_cinemas = db_service.get_all_cinemas(db)
    
    items: List[CinemaRead] = [
        CinemaRead(**dict_to_cinema_read(db_item))
        for db_item in db_cinemas
    ]
    
    if name:
        items = [c for c in items if name.lower() in c.name.lower()]
    
    return items


@router.get("/{cinema_id}", response_model=CinemaRead)
def get_cinema(
    cinema_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get a specific cinema from the database by ID."""
    db_service = CinemaDataService()
    cinema_id_int = int(str(cinema_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_cinema_by_id(db, cinema_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cinema not found")
    
    item = CinemaRead(**dict_to_cinema_read(db_item))
    etag = calc_etag(item)
    
    if if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})
    
    response.headers["ETag"] = etag
    return item


@router.patch("/{cinema_id}", response_model=CinemaRead)
def update_cinema(
    cinema_id: UUID,
    update: CinemaUpdate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Update a cinema (partial update) in the database."""
    db_service = CinemaDataService()
    cinema_id_int = int(str(cinema_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_cinema_by_id(db, cinema_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cinema not found")
    
    existing = CinemaRead(**dict_to_cinema_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    updates = update.model_dump(exclude_none=True)
    success = db_service.update_cinema(
        db=db,
        cinema_id=cinema_id_int,
        name=updates.get('name')
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update cinema")
    
    db_item = db_service.get_cinema_by_id(cinema_id_int)
    updated = CinemaRead(**dict_to_cinema_read(db_item))
    
    new_etag = calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated


@router.put("/{cinema_id}", response_model=CinemaRead)
def replace_cinema(
    cinema_id: UUID,
    cinema: CinemaCreate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Replace entire cinema resource (PUT) in the database."""
    db_service = CinemaDataService()
    cinema_id_int = int(str(cinema_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_cinema_by_id(db, cinema_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cinema not found")
    
    existing = CinemaRead(**dict_to_cinema_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.update_cinema(
        db=db,
        cinema_id=cinema_id_int,
        name=cinema.name
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to replace cinema")
    
    db_item = db_service.get_cinema_by_id(cinema_id_int)
    replacement = CinemaRead(**dict_to_cinema_read(db_item))
    
    new_etag = calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement


@router.delete("/{cinema_id}")
def delete_cinema(
    cinema_id: UUID,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Soft delete a cinema from the database."""
    db_service = CinemaDataService()
    cinema_id_int = int(str(cinema_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_cinema_by_id(db, cinema_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cinema not found")
    
    existing = CinemaRead(**dict_to_cinema_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.delete_cinema(db, cinema_id_int)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete cinema")
    
    return {"status": "deleted", "id": str(cinema_id)}
