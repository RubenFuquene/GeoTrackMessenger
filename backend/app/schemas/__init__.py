from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Location schemas
class LocationBase(BaseModel):
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    address: Optional[str] = None


class LocationCreate(LocationBase):
    timestamp: Optional[datetime] = None


class LocationResponse(LocationBase):
    id: int
    user_id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Geofence schemas
class GeofenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    center_latitude: float
    center_longitude: float
    radius: float


class GeofenceCreate(GeofenceBase):
    pass


class GeofenceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    center_latitude: Optional[float] = None
    center_longitude: Optional[float] = None
    radius: Optional[float] = None
    is_active: Optional[bool] = None


class GeofenceResponse(GeofenceBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Message schemas
class MessageBase(BaseModel):
    content: str
    message_type: str = "text"
    recipient_id: Optional[int] = None
    location_id: Optional[int] = None


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# User Geofence schemas
class UserGeofenceBase(BaseModel):
    geofence_id: int
    notification_enabled: bool = True
    enter_alert: bool = True
    exit_alert: bool = True


class UserGeofenceCreate(UserGeofenceBase):
    pass


class UserGeofenceResponse(UserGeofenceBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
