import os
import logging

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from app.config import get_settings

log = logging.getLogger("uvicorn")

settings = get_settings()

DATABASE_URL = settings.test_database_url if settings.testing else settings.database_url

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)

    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())