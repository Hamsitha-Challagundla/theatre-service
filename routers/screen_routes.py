"""Screen API endpoints - connected to database."""

from datetime import datetime
from typing import List, Optional
# IDs are integers now; no UUID import required

from fastapi import APIRouter, HTTPException, Header, Query, Depends
from fastapi.responses import Response

from schemas.screen import ScreenCreate, ScreenRead, ScreenUpdate
from services.screenDataService import ScreenDataService
from utils.etag import calc_etag
from utils.converters import dict_to_screen_read
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/screens", tags=["screens"])


@router.post("", response_model=ScreenRead, status_code=201)
def create_screen(screen: ScreenCreate, response: Response, db: Session = Depends(get_db)):
    """Create a new screen in the database."""
    db_service = ScreenDataService()
    
    screen_obj = db_service.create_screen(
        db=db,
        theatre_id=1,  # Placeholder - would map UUID to int
        screen_number=screen.screen_number,
        num_rows=screen.num_rows,
        num_cols=screen.num_cols,
        created_by=1  # Placeholder - would come from auth
    )
    
    # db_item = db_service.get_screen_by_id(screen_id)
    # if not db_item:
    #     raise HTTPException(status_code=500, detail="Failed to create screen")
    
    new_screen = ScreenRead(**dict_to_screen_read(screen_obj))
    response.headers["ETag"] = calc_etag(new_screen)
    return new_screen


@router.get("", response_model=List[ScreenRead])
def list_screens(
    theatre_id: Optional[int] = Query(None, description="Filter by theatre ID"),
    screen_number: Optional[int] = Query(None, description="Filter by screen number"),
    db: Session = Depends(get_db),
):
    """List all screens from the database with optional filtering."""
    db_service = ScreenDataService()
    db_screens = db_service.get_all_screens(db)
    
    items: List[ScreenRead] = [
        ScreenRead(**dict_to_screen_read(db_item))
        for db_item in db_screens
    ]
    
    if theatre_id:
        items = [s for s in items if s.theatre_id == theatre_id]
    if screen_number is not None:  # This line remains unchanged
        items = [s for s in items if s.screen_number == screen_number]
    
    return items


@router.get("/{screen_id}", response_model=ScreenRead)
def get_screen(
    screen_id: int,
    response: Response,
    if_none_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get a specific screen from the database by ID."""
    db_service = ScreenDataService()
    db_item = db_service.get_screen_by_id(db, screen_id)
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
    screen_id: int,
    update: ScreenUpdate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Update a screen (partial update) in the database."""
    db_service = ScreenDataService()
    db_item = db_service.get_screen_by_id(db, screen_id)
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
        db=db,
        screen_id=screen_id,
        screen_number=updates.get('screen_number'),
        num_rows=updates.get('num_rows'),
        num_cols=updates.get('num_cols')
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update screen")
    
    db_item = db_service.get_screen_by_id(db, screen_id)
    updated = ScreenRead(**dict_to_screen_read(db_item))
    
    new_etag = calc_etag(updated)
    response.headers["ETag"] = new_etag
    return updated


@router.put("/{screen_id}", response_model=ScreenRead)
def replace_screen(
    screen_id: int,
    screen: ScreenCreate,
    response: Response,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Replace entire screen resource (PUT) in the database."""
    db_service = ScreenDataService()
    db_item = db_service.get_screen_by_id(db, screen_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    existing = ScreenRead(**dict_to_screen_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is None:
        raise HTTPException(status_code=428, detail="Precondition Required: missing If-Match")
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.update_screen(
        db=db,
        screen_id=screen_id,
        screen_number=screen.screen_number,
        num_rows=screen.num_rows,
        num_cols=screen.num_cols
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to replace screen")
    
    db_item = db_service.get_screen_by_id(db, screen_id)
    replacement = ScreenRead(**dict_to_screen_read(db_item))
    
    new_etag = calc_etag(replacement)
    response.headers["ETag"] = new_etag
    return replacement


@router.delete("/{screen_id}")
def delete_screen(
    screen_id: int,
    if_match: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Soft delete a screen from the database."""
    db_service = ScreenDataService()
    db_item = db_service.get_screen_by_id(db, screen_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Screen not found")
    
    existing = ScreenRead(**dict_to_screen_read(db_item))
    current_etag = calc_etag(existing)
    
    if if_match is not None and if_match != current_etag:
        raise HTTPException(status_code=412, detail="Precondition Failed: ETag mismatch")
    
    success = db_service.delete_screen(db, screen_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete screen")
    
    return {"status": "deleted", "id": screen_id}
