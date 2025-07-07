import aiohttp
import asyncio
import logging
from datetime import datetime
from config import BACKEND_URL

logger = logging.getLogger(__name__)


class BackendService:
    """Service to communicate with the GeoTrack Messenger backend API."""
    
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def send_location(self, user_id: int, latitude: float, longitude: float, **kwargs):
        """Send location data to the backend."""
        try:
            session = await self._get_session()
            
            # For now, we'll store the location without authentication
            # In production, you'd want to implement proper user authentication
            location_data = {
                'latitude': latitude,
                'longitude': longitude,
                'timestamp': datetime.now().isoformat(),
                'telegram_user_id': user_id,
                **kwargs
            }
            
            async with session.post(
                f"{self.base_url}/locations/",
                json=location_data,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    logger.info(f"Location sent successfully for user {user_id}")
                    return True
                else:
                    logger.error(f"Failed to send location: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending location to backend: {e}")
            return False
    
    async def get_user_locations(self, user_id: int, limit: int = 10):
        """Get user's location history."""
        try:
            session = await self._get_session()
            
            async with session.get(
                f"{self.base_url}/locations/",
                params={'user_id': user_id, 'limit': limit}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get locations: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting locations from backend: {e}")
            return []
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
