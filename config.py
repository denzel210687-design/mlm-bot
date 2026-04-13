import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip()
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '').strip()
ADMIN_IDS = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip().isdigit()]
PANEL_PASSWORD = os.getenv('PANEL_PASSWORD', 'admin123').strip()
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-please').strip()
PORT = int(os.getenv('PORT', '8000'))
BOT_USERNAME = os.getenv('BOT_USERNAME', '').strip()
PROJECT_LINK_MASK = os.getenv('PROJECT_LINK_MASK', 'https://').strip()

def bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')

AI_ENABLED = bool_env('AI_ENABLED', True)
