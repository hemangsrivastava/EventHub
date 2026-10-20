
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_events():
    connection = sqlite3.connect("eventhub.db")
    connection.row_factory = sqlite3.Row

    events = connection.execute(
        "SELECT * FROM events ORDER BY event_date"
    ).fetchall()

    connection.close()
    return events


@app.route("/")
def home():
    events = get_events()
    return render_template("index.html", events=events)


if __name__ == "__main__":
    app.run(debug=True)
