from sqlalchemy.orm import Session
from sqlalchemy import func
from geopy.distance import geodesic
from typing import List

from app.models import Location, Geofence, UserGeofence, User


async def check_geofence_alerts(location: Location, db: Session):
    """
    Check if a location triggers any geofence alerts and send notifications.
    """
    # Get all active geofences
    geofences = db.query(Geofence).filter(
        Geofence.is_active == True
    ).all()
    
    for geofence in geofences:
        # Calculate distance using geopy
        location_point = (location.latitude, location.longitude)
        geofence_center = (geofence.center_latitude, geofence.center_longitude)
        distance = geodesic(location_point, geofence_center).meters
        
        # Check if user is within geofence
        is_inside = distance <= geofence.radius
        
        # Get user geofence settings
        user_geofence = db.query(UserGeofence).filter(
            UserGeofence.user_id == location.user_id,
            UserGeofence.geofence_id == geofence.id
        ).first()
        
        if user_geofence and user_geofence.notification_enabled:
            # Here you would typically:
            # 1. Check previous location to determine if this is an enter/exit event
            # 2. Send notification based on user preferences
            # 3. Log the event
            
            # For now, just print the alert (in production, use proper logging)
            if is_inside:
                print(f"User {location.user_id} entered geofence {geofence.name}")
            else:
                print(f"User {location.user_id} outside geofence {geofence.name}")


def calculate_distance_between_points(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using geodesic distance.
    Returns distance in meters.
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).meters


def is_point_in_geofence(lat: float, lon: float, geofence: Geofence) -> bool:
    """
    Check if a point is inside a geofence.
    """
    distance = calculate_distance_between_points(
        lat, lon, geofence.center_latitude, geofence.center_longitude
    )
    return distance <= geofence.radius


def find_nearby_users(location: Location, radius_meters: float, db: Session) -> List[User]:
    """
    Find users within a specified radius of a location.
    """
    # Get latest locations for all users
    latest_locations = db.query(Location).filter(
        Location.id.in_(
            db.query(func.max(Location.id)).group_by(Location.user_id)
        )
    ).all()
    
    nearby_users = []
    current_point = (location.latitude, location.longitude)
    
    for other_location in latest_locations:
        if other_location.user_id != location.user_id:
            other_point = (other_location.latitude, other_location.longitude)
            distance = geodesic(current_point, other_point).meters
            
            if distance <= radius_meters:
                user = db.query(User).filter(User.id == other_location.user_id).first()
                if user:
                    nearby_users.append(user)
    
    return nearby_users
