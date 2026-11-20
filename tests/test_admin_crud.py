
import sqlite3

import pytest

import app as app_module
import database as database_module


@pytest.fixture
def admin_crud_client(monkeypatch, tmp_path):
    # Create a separate database for testing.
    test_db = tmp_path / "admin_test.db"

    monkeypatch.setattr(
        app_module, "DATABASE_PATH", test_db
    )
    monkeypatch.setattr(
        database_module, "DATABASE_PATH", test_db
    )

    database_module.create_database()

    app_module.app.config.update(
        TESTING=True,
        SECRET_KEY="test-only-secret"
    )

    with app_module.app.test_client() as client:
        with client.session_transaction() as session:
            session["admin_logged_in"] = True

        yield client, test_db


def test_admin_can_create_event(admin_crud_client):
    client, test_db = admin_crud_client

    response = client.post(
        "/admin/add",
        data={
            "name": "DevOps Workshop",
            "description": "A workshop about CI/CD.",
            "event_date": "",
            "venue": "Computer Lab",
            "organizer": "DevOps Club",
            "category": "Technical",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/admin"
    )

    with sqlite3.connect(test_db) as connection:
        event = connection.execute(
            "SELECT name, description, venue "
            "FROM events WHERE name = ?",
            ("DevOps Workshop",),
        ).fetchone()

    assert event is not None
    assert event[0] == "DevOps Workshop"
    assert event[1] == "A workshop about CI/CD."
    assert event[2] == "Computer Lab"

def test_admin_can_edit_event(admin_crud_client):
    client, test_db = admin_crud_client

    # Insert an existing event into the test database.
    with sqlite3.connect(test_db) as connection:
        cursor = connection.execute(
            """
            INSERT INTO events
                (name, description, event_date,
                 venue, organizer, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Original Event",
                "Original description",
                "",
                "Old Venue",
                "DevOps Club",
                "Technical",
            ),
        )
        event_id = cursor.lastrowid

    # Admin edits the existing event.
    response = client.post(
        f"/admin/edit/{event_id}",
        data={
            "name": "Updated DevOps Workshop",
            "description": "Updated event description",
            "event_date": "",
            "venue": "New Computer Lab",
            "organizer": "DevOps Club",
            "category": "Technical",
        },
        follow_redirects=False,
    )

    # Verify successful redirect.
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin")

    # Verify updated data in SQLite.
    with sqlite3.connect(test_db) as connection:
        event = connection.execute(
            """
            SELECT name, description, venue
            FROM events
            WHERE id = ?
            """,
            (event_id,),
        ).fetchone()

    assert event is not None
    assert event[0] == "Updated DevOps Workshop"
    assert event[1] == "Updated event description"
    assert event[2] == "New Computer Lab"
