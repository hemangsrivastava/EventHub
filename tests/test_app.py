
import app as app_module


def test_homepage_returns_success(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "get_events",
        lambda search="", category="": ([], [])
    )

    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_homepage_renders_event(monkeypatch):
    event = {
        "id": 1,
        "name": "Test Event",
        "category": "Art & Culture",
        "description": "An event created for testing.",
        "event_date": "2099-01-01",
        "venue": "Test Venue",
        "organizer": "Test Organizer",
    }

    monkeypatch.setattr(
        app_module,
        "get_events",
        lambda search="", category="": ([event], ["Art & Culture"])
    )

    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Test Event" in response.data
    assert b"Test Venue" in response.data

def test_search_query_is_passed_to_backend(monkeypatch):
    captured = {}

    def fake_get_events(search="", category=""):
        captured["search"] = search
        captured["category"] = category
        return [], []

    monkeypatch.setattr(app_module, "get_events", fake_get_events)

    client = app_module.app.test_client()
    response = client.get("/?search=Chitrakala")

    assert response.status_code == 200
    assert captured["search"] == "Chitrakala"


def test_category_filter_is_passed_to_backend(monkeypatch):
    captured = {}

    def fake_get_events(search="", category=""):
        captured["search"] = search
        captured["category"] = category
        return [], []

    monkeypatch.setattr(app_module, "get_events", fake_get_events)

    client = app_module.app.test_client()
    response = client.get("/?category=Sports")

    assert response.status_code == 200
    assert captured["category"] == "Sports"


def test_combined_filters_are_passed_to_backend(monkeypatch):
    captured = {}

    def fake_get_events(search="", category=""):
        captured["search"] = search
        captured["category"] = category
        return [], []

    monkeypatch.setattr(app_module, "get_events", fake_get_events)

    client = app_module.app.test_client()
    response = client.get("/?search=Blood&category=Social+Impact")

    assert response.status_code == 200
    assert captured["search"] == "Blood"
    assert captured["category"] == "Social Impact"


def test_no_results_message_is_displayed(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "get_events",
        lambda search="", category="": ([], [])
    )

    client = app_module.app.test_client()
    response = client.get("/?search=NonexistentEvent")

    assert response.status_code == 200
    assert b"No events found" in response.data
