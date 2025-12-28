import sqlite3
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

DB_PATH = "storage/documents.db"
INDEX_PATH = "storage/vector_index.faiss"
META_PATH = "storage/vector_meta.json"

def build_index():
    print("🔧 Building FAISS vector index...")

    # Load embedding model (lightweight)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load blocks from SQLite
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, page_number, block_text FROM blocks")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("❌ No blocks found in database")
        return

    texts = [r[2] for r in rows]
    metadata = [{"block_id": r[0], "page": r[1]} for r in rows]

    # Create embeddings ONCE
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    Path("storage").mkdir(exist_ok=True)

    # Save index + metadata
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("✅ Vector DB created successfully")
    print(f"📦 Total vectors stored: {len(texts)}")

if __name__ == "__main__":
    build_index()
