import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

try:

    conn.execute("BEGIN")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
)
""")

    # raise KeyError("NOT FOUND")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT
)
""")

    conn.commit()

    print("Transaction Successful")

except Exception as e:

    conn.rollback()

    print("Transaction Failed")
    print(e)

finally:
    conn.close()