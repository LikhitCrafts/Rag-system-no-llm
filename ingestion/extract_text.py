import os
import fitz
import sqlite3

DB_PATH = "storage/documents.db"
PDF_DIR = "data/pdfs"


def extract_text_all_pdfs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT document_id, filename FROM documents")
    documents = cursor.fetchall()

    for document_id, filename in documents:
        pdf_path = os.path.join(PDF_DIR, filename)

        if not os.path.exists(pdf_path):
            print(f"⚠️ Missing file: {filename}")
            continue

        doc = fitz.open(pdf_path)

        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            text = page.get_text().strip()

            cursor.execute("""
                INSERT INTO pages (document_id, page_number, text)
                VALUES (?, ?, ?)
            """, (document_id, page_index + 1, text))

        print(f"✅ Text extracted: {filename} ({doc.page_count} pages)")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    extract_text_all_pdfs()
