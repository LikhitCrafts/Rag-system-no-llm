import sqlite3

KG_DB = "storage/knowledge_graph.db"


def kg_fact_lookup(question):
    if not question.lower().startswith(("what is", "define")):
        return []

    entity = question.lower().replace("what is", "").replace("define", "").strip(" ?")

    conn = sqlite3.connect(KG_DB)
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT subject, predicate, object FROM relations WHERE lower(subject) LIKE ?",
            (f"%{entity}%",)
        )
        rows = cur.fetchall()
    except:
        rows = []

    conn.close()

    return [f"{s} {p} {o}" for s, p, o in rows]
