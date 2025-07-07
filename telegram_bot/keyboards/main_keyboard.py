from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    """Get the main keyboard with location sharing button."""
    keyboard = [
        [KeyboardButton("📍 Share Location", request_location=True)],
        [KeyboardButton("📊 Status"), KeyboardButton("❓ Help")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_location_keyboard():
    """Get keyboard specifically for location sharing."""
    keyboard = [
        [KeyboardButton("📍 Share My Location", request_location=True)],
        [KeyboardButton("🔙 Back to Menu")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
