import faiss
import json
import numpy as np
import sqlite3

DB_PATH = "storage/documents.db"
INDEX_PATH = "storage/vector_index.faiss"
META_PATH = "storage/vector_meta.json"

_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def vector_search(question, top_k=3):
    model = get_model()

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    q_vec = model.encode([question]).astype("float32")
    distances, indices = index.search(q_vec, top_k)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    results = []

    for idx in indices[0]:
        meta = metadata[idx]
        cur.execute(
            "SELECT block_text FROM blocks WHERE id=?",
            (meta["block_id"],)
        )
        text = cur.fetchone()[0]
        results.append((meta["page"], text))

    conn.close()
    return results
