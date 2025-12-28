import sqlite3
import re

DB_PATH = "storage/documents.db"


def search_blocks(question, top_k=3):
    keywords = [k.lower() for k in re.findall(r"[A-Za-z@_]+", question) if len(k) > 2]

    if not keywords:
        return []

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT page_number, block_text FROM blocks")
    rows = cur.fetchall()
    conn.close()

    results = []

    for page, text in rows:
        score = 0
        text_lower = text.lower()

        for k in keywords:
            if k in text_lower:
                score += 2

        if score >= 3:
            results.append((score, page, text))

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_k]
