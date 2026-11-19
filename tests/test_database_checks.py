import sqlite3
import database as database_module


def test_database_table_creation(monkeypatch, tmp_path):
    test_db = tmp_path / "test_eventhub.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", test_db)
    database_module.create_database()

    with sqlite3.connect(test_db) as connection:
        result = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='events'"
        ).fetchone()

    assert result is not None


def test_sample_events_are_inserted(monkeypatch, tmp_path):
    test_db = tmp_path / "test_eventhub.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", test_db)
    database_module.initialize_database()

    with sqlite3.connect(test_db) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

    assert count == 3


def test_repeated_initialization_does_not_duplicate_events(monkeypatch, tmp_path):
    test_db = tmp_path / "test_eventhub.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", test_db)
    database_module.initialize_database()
    database_module.initialize_database()

    with sqlite3.connect(test_db) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

    assert count == 3