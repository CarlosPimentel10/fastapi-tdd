import os

import pytest
from starlette.testclient import TestClient

from app.config import Settings, get_settings
from app.db import init_db
from app.main import create_application


def get_settings_override():
    return Settings(
        testing=True,
        database_url=os.getenv("DATABASE_URL"),
        test_database_url=os.getenv("TEST_DATABASE_URL"),
    )


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    init_db(app, generate_schemas=True)

    with TestClient(app) as test_client:
        yield test_client
