import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")

class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    database_url: AnyUrl = "postgres://postgres:postgres@web-db:5432/web_dev"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()