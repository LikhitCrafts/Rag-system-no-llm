import sqlite3
import json
import os

DB_PATH = "storage/documents.db"
CHUNKS_PATH = "storage/chunks.json"


def store_chunks():
    if not os.path.exists(CHUNKS_PATH):
        print("❌ chunks.json not found")
        return

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ✅ CREATE blocks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT,
            page_number INTEGER,
            block_text TEXT
        )
    """)

    inserted = 0
    for ch in chunks:
        cur.execute(
            "INSERT INTO blocks (document_id, page_number, block_text) VALUES (?, ?, ?)",
            (ch["document_id"], ch["page"], ch["text"])
        )
        inserted += 1

    conn.commit()
    conn.close()

    print(f"✅ Stored {inserted} blocks into database")


if __name__ == "__main__":
    store_chunks()
