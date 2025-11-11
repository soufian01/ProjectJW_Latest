import sqlite3
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "coachkat.db"
SCHEMA_PATH = pathlib.Path(__file__).parent / "schema.sql"


def main():
    connection = sqlite3.connect(str(DB_PATH))
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    cursor = connection.cursor()
    video_count = cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    
    if video_count == 0:
        cursor.executemany(
            "INSERT INTO videos(title, url, durationSeconds) VALUES(?, ?, ?)",
            [
                ("Welcome to CoachKat", "/static/videos/How_Coaching_Works.mp4", 45),
                ("Focus Pomodoro Demo", "/static/videos/How_Coaching_Works.mp4", 60),
            ],
        )
    
    connection.commit()
    connection.close()
    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    main()
