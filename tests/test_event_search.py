
import sqlite3
import app as app_module
import database as database_module


def setup_test_database(monkeypatch, tmp_path):
    test_db = tmp_path / "test_events.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", test_db)
    monkeypatch.setattr(app_module, "DATABASE_PATH", test_db)

    database_module.initialize_database()

    return test_db


def test_search_by_event_name(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(search="Chitrakala")

    assert len(events) == 1
    assert events[0]["name"] == "Chitrakala"


def test_search_by_organizer(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(search="NSS")

    assert len(events) == 2


def test_filter_by_category(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(category="Sports")

    assert len(events) == 1
    assert events[0]["name"] == "Spandan"


def test_combined_search_and_category(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(
        search="Blood",
        category="Social Impact"
    )

    assert len(events) == 1
    assert events[0]["name"] == "Blood Donation Camp"
