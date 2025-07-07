from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2 import Geography
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.routes.users import get_current_user
from app.models import User, Location
from app.schemas import LocationCreate, LocationResponse
from app.utils.geofencing import check_geofence_alerts

router = APIRouter()


@router.post("/", response_model=LocationResponse)
async def create_location(
    location: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create location record
    db_location = Location(
        user_id=current_user.id,
        latitude=location.latitude,
        longitude=location.longitude,
        altitude=location.altitude,
        accuracy=location.accuracy,
        speed=location.speed,
        heading=location.heading,
        address=location.address,
        timestamp=location.timestamp or datetime.utcnow(),
        geom=func.ST_GeomFromText(f'POINT({location.longitude} {location.latitude})', 4326)
    )
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    # Check geofence alerts in background
    await check_geofence_alerts(db_location, db)
    
    return db_location


@router.get("/", response_model=List[LocationResponse])
async def read_locations(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Location)
    
    # Filter by user_id if provided and user has permission
    if user_id:
        if not current_user.is_admin and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        query = query.filter(Location.user_id == user_id)
    else:
        # Non-admin users can only see their own locations
        if not current_user.is_admin:
            query = query.filter(Location.user_id == current_user.id)
    
    locations = query.order_by(Location.timestamp.desc()).offset(skip).limit(limit).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
async def read_location(
    location_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Check permissions
    if not current_user.is_admin and location.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return location


@router.get("/user/{user_id}/latest", response_model=LocationResponse)
async def read_latest_location(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check permissions
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    location = db.query(Location).filter(
        Location.user_id == user_id
    ).order_by(Location.timestamp.desc()).first()
    
    if location is None:
        raise HTTPException(status_code=404, detail="No locations found for this user")
    
    return location
