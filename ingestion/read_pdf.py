import os
import uuid
import json
import sqlite3
import fitz  # PyMuPDF

PDF_DIR = "data/pdfs"
RAW_PAGES_PATH = "storage/raw_pages.json"
DB_PATH = "storage/documents.db"


def register_all_pdfs():
    os.makedirs("storage", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ CREATE documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT
        )
    """)

    pages = []

    print("🔍 Scanning for PDFs...")

    for filename in os.listdir(PDF_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_DIR, filename)
        doc_id = str(uuid.uuid4())

        cursor.execute(
            "INSERT OR REPLACE INTO documents (document_id, filename) VALUES (?, ?)",
            (doc_id, filename)
        )

        pdf = fitz.open(pdf_path)
        print(f"📄 Filename: {filename}")
        print(f"📑 Pages: {len(pdf)}")

        for i, page in enumerate(pdf):
            text = page.get_text()
            pages.append({
                "document_id": doc_id,
                "page": i + 1,
                "text": text
            })

        pdf.close()

    conn.commit()
    conn.close()

    with open(RAW_PAGES_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)

    print("✅ PDF Registered")


if __name__ == "__main__":
    register_all_pdfs()
