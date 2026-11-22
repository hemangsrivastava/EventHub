
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "eventhub.db"


def create_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                event_date TEXT,
                venue TEXT,
                organizer TEXT,
                category TEXT
            )
        """)


def insert_sample_events():
    sample_events = [
        (
            "Chitrakala",
            "A campus art and creativity event.",
            "2026-10-25",
            "Venue to be announced",
            "NSS",
            "Art & Culture",
        ),
        (
            "Blood Donation Camp",
            "A community initiative to support blood donation.",
            "2027-02-15",
            "Venue to be announced",
            "NSS",
            "Social Impact",
        ),
        (
            "Spandan",
            "A campus sports festival celebrating teamwork.",
            "2027-03-10",
            "Cricket Ground",
            "Sports Committee",
            "Sports",
        ),
    ]

    with sqlite3.connect(DATABASE_PATH) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

        if count == 0:
            connection.executemany("""
                INSERT INTO events
                    (name, description, event_date, venue, organizer, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, sample_events)


def initialize_database():
    create_database()
    insert_sample_events()


if __name__ == "__main__":
    initialize_database()
    print("EventHub database setup completed.")
