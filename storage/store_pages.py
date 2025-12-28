import sqlite3
from pathlib import Path

DB_PATH = Path("storage/documents.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_pages_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id TEXT,
        page_number INTEGER,
        text TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(document_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_pages_table()
    print("✅ Pages table ready")
