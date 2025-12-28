import sqlite3
import re

DOC_DB = "storage/documents.db"
KG_DB = "storage/knowledge_graph.db"

def clean(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def extract_relations(text):
    """
    Rule-based extractor:
    X is Y
    X provides Y
    X uses Y
    X includes Y
    """
    patterns = [
        r"(.+?) is (.+)",
        r"(.+?) provides (.+)",
        r"(.+?) uses (.+)",
        r"(.+?) includes (.+)"
    ]

    relations = []
    for p in patterns:
        m = re.match(p, text)
        if m:
            subj = clean(m.group(1))
            obj = clean(m.group(2))
            pred = p.split(" ")[1]
            relations.append((subj, pred, obj))
    return relations

def build_kg():
    print("🧠 Building CLEAN Knowledge Graph...")

    doc_conn = sqlite3.connect(DOC_DB)
    doc_cur = doc_conn.cursor()

    kg_conn = sqlite3.connect(KG_DB)
    kg_cur = kg_conn.cursor()

    kg_cur.execute("DROP TABLE IF EXISTS relations")
    kg_cur.execute("""
        CREATE TABLE relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            predicate TEXT,
            object TEXT,
            document_id TEXT
        )
    """)
    kg_conn.commit()

    doc_cur.execute("SELECT document_id, block_text FROM blocks")
    rows = doc_cur.fetchall()

    total = 0

    for document_id, text in rows:
        sentences = re.split(r"[.\n]", text)

        for s in sentences:
            s = clean(s)

            # 🔥 QUALITY FILTERS (IMPORTANT)
            if len(s) < 30:
                continue
            if s.endswith((" is", " is a", " is an")):
                continue
            if s.startswith(("•", "-", "●")):
                continue

            rels = extract_relations(s)
            for subj, pred, obj in rels:
                kg_cur.execute(
                    "INSERT INTO relations (subject, predicate, object, document_id) VALUES (?, ?, ?, ?)",
                    (subj, pred, obj, document_id)
                )
                total += 1

    kg_conn.commit()
    doc_conn.close()
    kg_conn.close()

    print(f"✅ KG created with {total} clean relations")

if __name__ == "__main__":
    build_kg()
