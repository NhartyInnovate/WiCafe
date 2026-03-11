import sqlite3

conn = sqlite3.connect("cafes.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables:")
for table in tables:
    print(table)

for table in tables:
    table_name = table[0]
    print(f"\nColumns in {table_name}:")
    cursor.execute(f"PRAGMA table_info({table_name});")
    for column in cursor.fetchall():
        print(column)

conn.close()