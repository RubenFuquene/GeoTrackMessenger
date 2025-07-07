from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_keyboard import get_main_keyboard
from services.backend_service import BackendService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n"
        f"Welcome to GeoTrack Messenger Bot! 🗺️\n\n"
        f"I can help you:\n"
        f"• Share your location\n"
        f"• Track your location history\n"
        f"• Send location-based messages\n\n"
        f"Use /help to see all available commands.",
        reply_markup=get_main_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 *GeoTrack Messenger Bot Commands*

📍 *Location Commands:*
/location - Share your current location
/status - Check your location sharing status

💬 *General Commands:*
/start - Start the bot
/help - Show this help message

📲 *How to use:*
1. Send your location using the 📍 button
2. Use commands to manage your location sharing
3. Your location will be saved to the GeoTrack system

💡 *Tips:*
• Enable location sharing in your Telegram settings
• Use the keyboard buttons for quick actions
• Your location data is securely stored
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /location command."""
    await update.message.reply_text(
        "Please share your location using the 📍 button below, or send a location message.",
        reply_markup=get_main_keyboard()
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user's location sharing status."""
    user_id = update.effective_user.id
    
    # Here you would check with the backend service
    # For now, we'll show a simple status message
    await update.message.reply_text(
        f"📊 *Your Status:*\n\n"
        f"🆔 Telegram ID: `{user_id}`\n"
        f"✅ Bot Status: Active\n"
        f"📍 Location Sharing: Enabled\n\n"
        f"Use /location to share your current position.",
        parse_mode='Markdown'
    )
