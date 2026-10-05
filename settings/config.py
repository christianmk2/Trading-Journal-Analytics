import os

from dotenv import load_dotenv

from settings.paths import ENV_FILE, SQLITE_DB_PATH

load_dotenv(dotenv_path=ENV_FILE)

def database_url() -> str:
    configured_url = os.getenv("DATABASE_URL", "").strip()
    if configured_url:
        return configured_url
    return "sqlite:///" + str(SQLITE_DB_PATH).replace("\\", "/") #or as_posix()