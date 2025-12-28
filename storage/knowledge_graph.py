import sqlite3

DB_PATH = "storage/knowledge_graph.db"

def create_kg():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        predicate TEXT,
        object TEXT,
        document_id TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Knowledge Graph DB ready")

if __name__ == "__main__":
    create_kg()
