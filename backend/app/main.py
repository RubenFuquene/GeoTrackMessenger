from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth, users, locations, geofences


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting GeoTrackMessenger API...")
    yield
    # Shutdown
    print("Shutting down GeoTrackMessenger API...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="GeoTrackMessenger - Location tracking and messaging API",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["locations"])
app.include_router(geofences.router, prefix="/api/v1/geofences", tags=["geofences"])


@app.get("/")
async def root():
    return {"message": "GeoTrackMessenger API is running!", "version": settings.APP_VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "GeoTrackMessenger API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
