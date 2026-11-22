
import pytest

import app as app_module
import database as database_module


@pytest.fixture
def client():
    """Provide a reusable Flask test client."""
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def test_db(monkeypatch, tmp_path):
    """Create an isolated SQLite database."""
    db_path = tmp_path / "test_eventhub.db"

    monkeypatch.setattr(
        database_module,
        "DATABASE_PATH",
        db_path
    )

    monkeypatch.setattr(
        app_module,
        "DATABASE_PATH",
        db_path
    )

    database_module.initialize_database()

    return db_path
