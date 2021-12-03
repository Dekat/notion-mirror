from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from notion_mirror.controllers import endpoints


@pytest.fixture(scope="session")
def app() -> Flask:
    """Session-wide test `Flask` application."""
    return endpoints.app


@pytest.fixture(scope="function")
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    """Return a Flask test client.

    An instance of :class:`flask.testing.TestClient` by default.
    """
    with app.test_client() as client:
        yield client
