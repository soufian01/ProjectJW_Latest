from flask import Flask, jsonify, request, send_from_directory
import sqlite3, pathlib, os

BASE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = BASE / "coachkat.db"

app = Flask(__name__, static_folder=str(BASE / "static"))

def db():
    # use string path and a small timeout for robustness across Python versions
    con = sqlite3.connect(str(DB_PATH), timeout=30)
    con.row_factory = sqlite3.Row
    return con

@app.get("/api/videos")
def api_videos():
    with db() as con:
        rows = con.execute("SELECT id,title,url,durationSeconds FROM videos ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/")
def index():
    # serve the simple frontend that fetches /api/videos
    return send_from_directory(str(pathlib.Path(__file__).resolve().parent.parent / "templates"), "index.html")

@app.post("/api/contact")
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not email or not message or "@" not in email:
        return jsonify({"ok": False, "error": "Invalid input"}), 400
    with db() as con:
        con.execute("INSERT INTO messages(name,email,message) VALUES(?,?,?)", (name, email, message))
        con.commit()
    return jsonify({"ok": True})


@app.get("/api/find-us")
def api_find_us():
    # static place — change to config/DB as needed
    place = {
        "name": "CoachKat Office",
        "address": "123 Main St, Anytown",
        "lat": 37.4224764,
        "lng": -122.0842499,
    }
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lng']}"
    result = {
        "name": place["name"],
        "address": place["address"],
        "lat": place["lat"],
        "lng": place["lng"],
        "maps_url": maps_url,
    }
    # If you provide an API key, include an embed URL for an interactive iframe.
    # Note: embedding exposes the key in page source — restrict the key by HTTP referrers.
    if api_key:
        result["embed_url"] = (
            f"https://www.google.com/maps/embed/v1/place"
            f"?key={api_key}&q={place['lat']},{place['lng']}&zoom=15"
        )
    return jsonify(result)

#@app.get("/static/<path:path>")
#def static_files(path):
#    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
