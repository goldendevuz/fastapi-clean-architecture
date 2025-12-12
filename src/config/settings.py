from typing import Literal
from datetime import timezone
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parent.parent.parent


class Env(BaseSettings):

    # System settings
    DEBUG: Literal["true", "false"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    # Database settings
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env"
    )


env = Env()  # type: ignore  # noqa

# System settings
DEBUG: bool = env.DEBUG == "true"
TIMEZONE = timezone.utc

# Logging settings
LOG_LEVEL = env.LOG_LEVEL
LOG_FILE_PATH = ROOT / "resources" / "app.log"
LOG_FORMAT = "[%(asctime)s] %(levelname)s in %(name)s:%(lineno)d — %(message)s"

# Database settings
DATABASE_USER = env.DATABASE_USER 
DATABASE_PASSWORD = env.DATABASE_PASSWORD
DATABASE_HOST = env.DATABASE_HOST
DATABASE_PORT = env.DATABASE_PORT
DATABASE_NAME = env.DATABASE_NAME 
