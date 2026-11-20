
import sqlite3
from contextlib import closing

from flask import Flask, render_template, request
from database import initialize_database, DATABASE_PATH

app = Flask(__name__)


def get_events(search="", category=""):
    query = "SELECT * FROM events WHERE 1=1"
    parameters = []

    if search:
        query += """
            AND (
                name LIKE ?
                OR description LIKE ?
                OR organizer LIKE ?
            )
        """
        search_term = f"%{search}%"
        parameters.extend([search_term, search_term, search_term])

    if category:
        query += " AND category = ?"
        parameters.append(category)

    query += " ORDER BY event_date"

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        events = connection.execute(
            query, parameters
        ).fetchall()

        categories = connection.execute(
            "SELECT DISTINCT category FROM events "
            "WHERE category IS NOT NULL AND category != '' "
            "ORDER BY category"
        ).fetchall()

    return events, [row["category"] for row in categories]


def get_event_by_id(event_id):
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        event = connection.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()

    return event


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    events, categories = get_events(search, category)

    return render_template(
        "index.html",
        events=events,
        categories=categories,
        search=search,
        selected_category=category
    )


@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        return render_template("404.html"), 404

    return render_template("event_detail.html", event=event)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
