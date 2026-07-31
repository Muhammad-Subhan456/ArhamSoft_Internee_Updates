import sqlite3

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
)
""")

tasks = [
    ("Learn FastAPI", 0, "2026-07-31"),
    ("Practice SQL", 0, "2026-07-31"),
    ("Build CRUD API", 1, "2026-07-31"),
]

cursor.executemany(
    """
    INSERT INTO tasks(title, done, created_at)
    VALUES (?, ?, ?)
    """,
    tasks,
)

connection.commit()

cursor.execute(
    "SELECT * FROM tasks WHERE done = ?",
    (0,),
)

print("Pending Tasks:")

for row in cursor.fetchall():
    print(row)

cursor.execute(
    """
    UPDATE tasks
    SET done = ?
    WHERE title = ?
    """,
    (1, "Practice SQL"),
)

connection.commit()

cursor.execute(
    """
    DELETE FROM tasks
    WHERE title = ?
    """,
    ("Learn FastAPI",),
)

connection.commit()

cursor.execute("SELECT * FROM tasks")

print("\nRemaining Tasks:")

for row in cursor.fetchall():
    print(row)

connection.close()