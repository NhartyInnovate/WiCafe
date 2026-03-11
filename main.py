import sqlite3


conn = sqlite3.connect("cafes.db")
cursor = conn.cursor


# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())


# Show columns in the cafe table
cursor.execute("PRAGMA table_info(cafe);")
for column in cursor.fetchall():
    print(column)

conn.close()
