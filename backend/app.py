from flask import Flask, jsonify, render_template
import os
import sqlite3
import pathlib

# Paths
BASE = pathlib.Path(__file__).resolve().parent.parent  # project root
DB_PATH = BASE / "coachkat.db"

# Serve root-level /static and /templates
app = Flask(
    __name__,
    static_folder=str(BASE / "static"),
    static_url_path="/static",
    template_folder=str(BASE / "templates"),
)

def db():
    con = sqlite3.connect(str(DB_PATH), timeout=30)
    con.row_factory = sqlite3.Row
    return con

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/videos")
def api_videos():
    with db() as con:
        rows = con.execute(
            "SELECT id, title, url, durationSeconds FROM videos ORDER BY id"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1").lower() in ("1", "true", "yes")
    print(f"Static -> {app.static_folder}")
    print(f"Templates -> {app.template_folder}")
    print(f"DB -> {DB_PATH}")
    app.run(host=host, port=port, debug=debug)
