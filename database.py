import sqlite3

# Connect to SQLite database (creates users.db if not exists)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

conn.commit()
conn.close()

print("Database initialized successfully!")
