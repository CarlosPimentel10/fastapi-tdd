import logging

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings

log = logging.getLogger("uvicorn")


def get_tortoise_config():
    settings = get_settings()

    database_url = settings.test_database_url if settings.testing else settings.database_url

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    return {
        "connections": {"default": database_url},
        "apps": {
            "models": {
                "models": ["app.models.tortoise", "aerich.models"],
                "default_connection": "default",
            },
        },
    }


def init_db(app: FastAPI, generate_schemas: bool = False) -> None:
    register_tortoise(
        app,
        config=get_tortoise_config(),
        generate_schemas=generate_schemas,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")
    await Tortoise.init(config=get_tortoise_config())

    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())