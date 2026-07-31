import sqlite3

conn = sqlite3.connect("tasks_vulnerable.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    title TEXT
)
""")

cursor.execute(
    "INSERT INTO tasks(title) VALUES (?)",
    ("Learn FastAPI",)
)

conn.commit()

cursor.execute("Select * from tasks")

title = input("Enter title: ")

# Wrong: User can SQL Inject and Can Damage The Database

# query = f"""
# SELECT *
# FROM tasks
# WHERE title = '{title}'
# """

# print(query)

# Solution: Use PlaceHolders

cursor.execute(
    """
    SELECT *
    FROM tasks
    WHERE title = ?
    """,
    (title,)
)