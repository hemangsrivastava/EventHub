
import sqlite3
import app as app_module
import database as database_module


def setup_test_database(monkeypatch, tmp_path):
    test_db = tmp_path / "test_events.db"

    monkeypatch.setattr(
        database_module, "DATABASE_PATH", test_db
    )
    monkeypatch.setattr(
        app_module, "DATABASE_PATH", test_db
    )

    database_module.initialize_database()

    return test_db


# Existing tests

def test_search_by_event_name(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(
        search="Chitrakala"
    )

    assert len(events) == 1
    assert events[0]["name"] == "Chitrakala"


def test_search_by_organizer(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(
        search="NSS"
    )

    assert len(events) == 2


def test_filter_by_category(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events(
        category="Sports"
    )

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


# Commit #3: Search edge case tests

def test_search_is_case_insensitive(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events_lower, _ = app_module.get_events(
        search="chitrakala"
    )
    events_upper, _ = app_module.get_events(
        search="CHITRAKALA"
    )

    assert len(events_lower) == 1
    assert len(events_upper) == 1
    assert events_lower[0]["name"] == "Chitrakala"
    assert events_upper[0]["name"] == "Chitrakala"


def test_partial_event_name_search(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(
        search="Chitra"
    )

    assert len(events) == 1
    assert events[0]["name"] == "Chitrakala"


def test_nonexistent_event_search(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(
        search="UnknownEvent123"
    )

    assert len(events) == 0


def test_empty_search_returns_all_events(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(
        search=""
    )

    assert len(events) == 3


def test_invalid_category_returns_no_events(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(
        category="UnknownCategory"
    )

    assert len(events) == 0


def test_empty_category_returns_all_events(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(category="")

    assert len(events) == 3


def test_category_filter_excludes_other_categories(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(category="Sports")

    assert len(events) == 1
    assert all(event["category"] == "Sports" for event in events)


def test_mismatched_search_and_category(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, _ = app_module.get_events(
        search="Chitrakala",
        category="Sports"
    )

    assert len(events) == 0


def test_available_categories_are_unique_and_sorted(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    events, categories = app_module.get_events()

    assert categories == [
        "Art & Culture",
        "Social Impact",
        "Sports"
    ]
    assert len(categories) == len(set(categories))

