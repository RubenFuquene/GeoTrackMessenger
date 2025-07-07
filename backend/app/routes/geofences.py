from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.routes.users import get_current_user
from app.models import User, Geofence
from app.schemas import GeofenceCreate, GeofenceUpdate, GeofenceResponse

router = APIRouter()


@router.post("/", response_model=GeofenceResponse)
async def create_geofence(
    geofence: GeofenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_geofence = Geofence(
        user_id=current_user.id,
        name=geofence.name,
        description=geofence.description,
        center_latitude=geofence.center_latitude,
        center_longitude=geofence.center_longitude,
        radius=geofence.radius,
        geom=func.ST_GeomFromText(f'POINT({geofence.center_longitude} {geofence.center_latitude})', 4326)
    )
    
    db.add(db_geofence)
    db.commit()
    db.refresh(db_geofence)
    
    return db_geofence


@router.get("/", response_model=List[GeofenceResponse])
async def read_geofences(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Geofence)
    
    # Non-admin users can only see their own geofences
    if not current_user.is_admin:
        query = query.filter(Geofence.user_id == current_user.id)
    
    geofences = query.offset(skip).limit(limit).all()
    return geofences


@router.get("/{geofence_id}", response_model=GeofenceResponse)
async def read_geofence(
    geofence_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    geofence = db.query(Geofence).filter(Geofence.id == geofence_id).first()
    if geofence is None:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    # Check permissions
    if not current_user.is_admin and geofence.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return geofence


@router.put("/{geofence_id}", response_model=GeofenceResponse)
async def update_geofence(
    geofence_id: int,
    geofence_update: GeofenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    geofence = db.query(Geofence).filter(Geofence.id == geofence_id).first()
    if geofence is None:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    # Check permissions
    if not current_user.is_admin and geofence.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = geofence_update.dict(exclude_unset=True)
    
    # Update geometry if coordinates changed
    if 'center_latitude' in update_data or 'center_longitude' in update_data:
        lat = update_data.get('center_latitude', geofence.center_latitude)
        lon = update_data.get('center_longitude', geofence.center_longitude)
        update_data['geom'] = func.ST_GeomFromText(f'POINT({lon} {lat})', 4326)
    
    for field, value in update_data.items():
        setattr(geofence, field, value)
    
    db.commit()
    db.refresh(geofence)
    return geofence


@router.delete("/{geofence_id}")
async def delete_geofence(
    geofence_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    geofence = db.query(Geofence).filter(Geofence.id == geofence_id).first()
    if geofence is None:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    # Check permissions
    if not current_user.is_admin and geofence.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(geofence)
    db.commit()
    return {"message": "Geofence deleted successfully"}
