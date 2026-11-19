
import sqlite3
from contextlib import closing

from flask import Flask, render_template
from database import initialize_database, DATABASE_PATH

app = Flask(__name__)


def get_events():
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        events = connection.execute(
            "SELECT * FROM events ORDER BY event_date"
        ).fetchall()

    return events


@app.route("/")
def home():
    events = get_events()
    return render_template("index.html", events=events)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
