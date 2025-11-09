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
                ("Welcome to CoachKat", "/static/videos/introduction.mp4", 45),
                ("Most Important Organ", "/static/videos/most_important_organ.mp4", 60),
            ],
        )
    con.commit()
    con.close()
    print(f"Initialized {DB_PATH}")

if __name__ == "__main__":
    main()
