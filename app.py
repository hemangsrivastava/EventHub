
import os
import sqlite3
from contextlib import closing
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)

from database import initialize_database, DATABASE_PATH

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "eventhub-development-key")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "eventhub123")


# =========================================
# DATABASE FUNCTIONS
# =========================================

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

        events = connection.execute(query, parameters).fetchall()

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


# =========================================
# ADMIN ACCESS PROTECTION
# =========================================

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return function(*args, **kwargs)

    return wrapper


# =========================================
# HOMEPAGE
# =========================================

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


# =========================================
# INDIVIDUAL EVENT PAGE
# =========================================

@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        return render_template("404.html"), 404

    return render_template("event_detail.html", event=event)


# =========================================
# ADMIN LOGIN
# =========================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Incorrect username or password."
        )

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route("/admin")
@admin_required
def admin_dashboard():
    events, categories = get_events()

    return render_template(
        "admin_dashboard.html",
        events=events
    )


# =========================================
# ADD EVENT
# =========================================

@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def add_event():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        event_date = request.form.get("event_date", "").strip()
        venue = request.form.get("venue", "").strip()
        organizer = request.form.get("organizer", "").strip()
        category = request.form.get("category", "").strip()

        if not name or not description:
            return render_template(
                "admin_event_form.html",
                event=request.form,
                page_title="Add Event",
                error="Event name and description are required."
            )

        with closing(sqlite3.connect(DATABASE_PATH)) as connection:
            connection.execute("""
                INSERT INTO events
                (name, description, event_date, venue, organizer, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, description, event_date,
                venue, organizer, category
            ))
            connection.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin_event_form.html",
        event=None,
        page_title="Add Event"
    )


# =========================================
# EDIT EVENT
# =========================================

@app.route("/admin/edit/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    event = get_event_by_id(event_id)

    if event is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        event_date = request.form.get("event_date", "").strip()
        venue = request.form.get("venue", "").strip()
        organizer = request.form.get("organizer", "").strip()
        category = request.form.get("category", "").strip()

        if not name or not description:
            return render_template(
                "admin_event_form.html",
                event=request.form,
                page_title="Edit Event",
                error="Event name and description are required."
            )

        with closing(sqlite3.connect(DATABASE_PATH)) as connection:
            connection.execute("""
                UPDATE events
                SET name = ?, description = ?, event_date = ?,
                    venue = ?, organizer = ?, category = ?
                WHERE id = ?
            """, (
                name, description, event_date,
                venue, organizer, category, event_id
            ))
            connection.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin_event_form.html",
        event=event,
        page_title="Edit Event"
    )


# =========================================
# DELETE EVENT
# =========================================

@app.route("/admin/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.execute(
            "DELETE FROM events WHERE id = ?",
            (event_id,)
        )
        connection.commit()

    return redirect(url_for("admin_dashboard"))


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
