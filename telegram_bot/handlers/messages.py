from telegram import Update
from telegram.ext import ContextTypes
from services.backend_service import BackendService
import logging

logger = logging.getLogger(__name__)


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle location messages."""
    user = update.effective_user
    location = update.message.location
    
    logger.info(f"Received location from user {user.id}: {location.latitude}, {location.longitude}")
    
    try:
        # Send location to backend service
        backend_service = BackendService()
        success = await backend_service.send_location(
            user_id=user.id,
            latitude=location.latitude,
            longitude=location.longitude
        )
        
        if success:
            await update.message.reply_text(
                f"📍 *Location Received!*\n\n"
                f"🌍 Latitude: `{location.latitude:.6f}`\n"
                f"🌍 Longitude: `{location.longitude:.6f}`\n\n"
                f"✅ Your location has been saved to GeoTrack Messenger!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Sorry, there was an error saving your location. Please try again later."
            )
    
    except Exception as e:
        logger.error(f"Error handling location: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred. Please try again later."
        )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text.lower()
    
    if "location" in text or "where" in text:
        await update.message.reply_text(
            "To share your location, please use the 📍 button in your Telegram keyboard, "
            "or use the /location command for more options."
        )
    elif "help" in text:
        await update.message.reply_text(
            "Use /help to see all available commands, or /start to begin using the bot."
        )
    else:
        await update.message.reply_text(
            "I'm a location tracking bot! 🗺️\n\n"
            "Send me your location or use /help to see what I can do."
        )
