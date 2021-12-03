import os
import sys

from environs import Env


env = Env()
env.read_env()

APP_PATH = os.path.dirname(sys.argv[0])

# Flask
FLASK_DEBUG = env.bool("FLASK_DEBUG", False)
FLASK_PORT = env.int("PORT")
SECRET_KEY = env.str("SECRET_KEY")
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", None)

# Logging
LOG_LEVEL = env.str("LOG_LEVEL")

# Caching
CACHE_FOLDER = env.str("CACHE_FOLDER", os.path.join(APP_PATH, "cache"))
CACHE_ASSETS_FOLDER = env.str(
    "CACHE_ASSETS_FOLDER", os.path.join(CACHE_FOLDER, "assets")
)
os.makedirs(CACHE_ASSETS_FOLDER, exist_ok=True)

# Cors
CORS_MAX_AGE = env.int("CORS_MAX_AGE")
CORS_ORIGINS = env.str("CORS_ORIGINS")
CORS_SUPPORTS_CREDENTIALS = env.bool("CORS_SUPPORTS_CREDENTIALS")

# Notion
NOTION_API_TOKEN = env.str("NOTION_API_TOKEN")
NOTION_SPACE_ID = env.str("NOTION_SPACE_ID")
