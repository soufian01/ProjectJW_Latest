import sqlite3, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent  # project root
DB_PATH = BASE / "coachkat.db"
SCHEMA = pathlib.Path(__file__).with_name("Schema.sql")

def main():
    con = sqlite3.connect(DB_PATH)
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())

    cur = con.cursor()
    count = cur.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO videos(title, url, durationSeconds) VALUES(?,?,?)",
            [
                ("Welcome to CoachKat", "/static/videos/How_Coaching_Works.mp4", 45),
                ("Focus Pomodoro Demo", "/static/videos/How_Coaching_Works.mp4", 60),
            ],
        )
    con.commit()
    con.close()
    print(f"Initialized {DB_PATH}")

if __name__ == "__main__":
    main()
