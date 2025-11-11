from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "coachkat.db"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = Flask(__name__, static_folder=str(STATIC_DIR))


def get_db_connection():
    connection = sqlite3.connect(str(DB_PATH), timeout=30)
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/")
def index():
    return send_from_directory(str(TEMPLATES_DIR), "index.html")


@app.get("/api/videos")
def api_videos():
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, url, durationSeconds FROM videos ORDER BY id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/contact")
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    
    if not name or not email or not message or "@" not in email:
        return jsonify({"ok": False, "error": "Invalid input"}), 400
    
    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO messages(name, email, message) VALUES(?, ?, ?)",
            (name, email, message)
        )
        connection.commit()
    
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
