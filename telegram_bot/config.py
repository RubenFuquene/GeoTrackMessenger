import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL')

# Backend API configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/api/v1')

# Bot settings
POLL_INTERVAL = 1.0
TIMEOUT = 30
