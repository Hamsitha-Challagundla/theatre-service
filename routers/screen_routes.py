"""Screen API endpoints - connected to database."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Header, Query
from fastapi.responses import Response

from schemas.screen import ScreenCreate, ScreenRead, ScreenUpdate
from services.screenDataService import ScreenDataService
from utils.etag import calc_etag
from utils.converters import dict_to_screen_read


router = APIRouter(prefix="/screens", tags=["screens"])


@router.post("", response_model=ScreenRead, status_code=201)
def create_screen(screen: ScreenCreate, response: Response):
    """Create a new screen in the database."""
    db_service = ScreenDataService()
    
    screen_id = db_service.create_screen(
        theatre_id=1,  # Placeholder - would map UUID to int
        screen_number=screen.screen_number,
        num_rows=screen.num_rows,
        num_cols=screen.num_cols,
        created_by=1  # Placeholder - would come from auth
    )
    
    db_item = db_service.get_screen_by_id(screen_id)
    if not db_item:
        raise HTTPException(status_code=500, detail="Failed to create screen")
    
    new_screen = ScreenRead(**dict_to_screen_read(db_item))
    response.headers["ETag"] = calc_etag(new_screen)
    return new_screen


@router.get("", response_model=List[ScreenRead])
def list_screens(
    theatre_id: Optional[UUID] = Query(None, description="Filter by theatre ID"),
    screen_number: Optional[int] = Query(None, description="Filter by screen number"),
):
    """List all screens from the database with optional filtering."""
    db_service = ScreenDataService()
    db_screens = db_service.get_all_screens()
    
    items: List[ScreenRead] = [
        ScreenRead(**dict_to_screen_read(db_item))
        for db_item in db_screens
    ]
    
    if theatre_id:
        items = [s for s in items if s.theatre_id == theatre_id]
    if screen_number is not None:
        items = [s for s in items if s.screen_number == str(screen_number)]
    
    return items


@router.get("/{screen_id}", response_model=ScreenRead)
def get_screen(
    screen_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None)
):
    """Get a specific screen from the database by ID."""
    db_service = ScreenDataService()
    screen_id_int = int(str(screen_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    item = ScreenRead(**dict_to_screen_read(db_item))
    etag = calc_etag(item)
    
    if if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})
    
    response.headers["ETag"] = etag
    return item


@router.patch("/{screen_id}", response_model=ScreenRead)
def update_screen(
    screen_id: UUID,
    update: ScreenUpdate,
    response: Response,
    if_match: Optional[str] = Header(None)
):
    """Update a screen (partial update) in the database."""
    db_service = ScreenDataService()
    screen_id_int = int(str(screen_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    existing = ScreenRead(**dict_to_screen_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    updates = update.model_dump(exclude_none=True)
    success = db_service.update_screen(
        screen_id=screen_id_int,
        screen_number=updates.get('screen_number'),
        num_rows=updates.get('num_rows'),
        num_cols=updates.get('num_cols')
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update screen")
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    updated = ScreenRead(**dict_to_screen_read(db_item))
    
    new_etag = calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated


@router.put("/{screen_id}", response_model=ScreenRead)
def replace_screen(
    screen_id: UUID,
    screen: ScreenCreate,
    response: Response,
    if_match: Optional[str] = Header(None)
):
    """Replace entire screen resource (PUT) in the database."""
    db_service = ScreenDataService()
    screen_id_int = int(str(screen_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    existing = ScreenRead(**dict_to_screen_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.update_screen(
        screen_id=screen_id_int,
        screen_number=screen.screen_number,
        num_rows=screen.num_rows,
        num_cols=screen.num_cols
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to replace screen")
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    replacement = ScreenRead(**dict_to_screen_read(db_item))
    
    new_etag = calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement


@router.delete("/{screen_id}")
def delete_screen(
    screen_id: UUID,
    if_match: Optional[str] = Header(None)
):
    """Soft delete a screen from the database."""
    db_service = ScreenDataService()
    screen_id_int = int(str(screen_id).replace('-', '')[:8], 16) % (10**9)
    
    db_item = db_service.get_screen_by_id(screen_id_int)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    existing = ScreenRead(**dict_to_screen_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.delete_screen(screen_id_int)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete screen")
    
    return {"status": "deleted", "id": str(screen_id)}
