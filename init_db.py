import sqlite3

conn = sqlite3.connect("network.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS logs")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    upload REAL,
    download REAL,
    total REAL,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database fully fixed!")