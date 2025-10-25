import sqlite3

DATABASE = "bdd.db"

def rebuild_database():
    """
    Drops all existing tables (if any) and recreates a fresh schema
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS Answer")
        cursor.execute("DROP TABLE IF EXISTS Question")
        cursor.execute("DROP TABLE IF EXISTS Player")

        cursor.execute("""
            CREATE TABLE Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'easy',
                image BLOB,
                position INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE Answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                isCorrect INTEGER NOT NULL CHECK (isCorrect IN (0, 1)),
                text TEXT NOT NULL,
                FOREIGN KEY(question_id) REFERENCES Question(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playerName TEXT NOT NULL,
                answers TEXT,
                score INTEGER DEFAULT 0
            )
        """)

        conn.commit()
        print("Database rebuilt successfully.")
        return True

    except Exception as e:
        print(f"Error rebuilding database: {e}")
        return False

    finally:
        conn.close()

if __name__ == "__main__":
    success = rebuild_database()
    if success:
        print("Database schema generated successfully.")
    else:
        print("Database generation failed.")
