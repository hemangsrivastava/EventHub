
import sqlite3

import app as app_module


def test_homepage_returns_success(monkeypatch):
    monkeypatch.setattr(app_module, "get_events", lambda: [])

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

    monkeypatch.setattr(app_module, "get_events", lambda: [event])

    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Test Event" in response.data
    assert b"Test Venue" in response.data
