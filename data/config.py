import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN = os.getenv("ADMIN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")