import json
import os
import re

INPUT_PATH = "storage/raw_pages.json"
OUTPUT_PATH = "storage/chunks.json"
CHUNK_SIZE = 400


def chunk_text(text):
    words = text.split()
    chunks = []

    for i in range(0, len(words), CHUNK_SIZE):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        if len(chunk.strip()) > 50:
            chunks.append(chunk)

    return chunks


def chunk_pages():
    if not os.path.exists(INPUT_PATH):
        print("❌ raw_pages.json not found")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)

    all_chunks = []

    for page in pages:
        clean_text = re.sub(r"\s+", " ", page["text"]).strip()
        chunks = chunk_text(clean_text)

        for ch in chunks:
            all_chunks.append({
                "document_id": page["document_id"],
                "page": page["page"],
                "text": ch
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"✅ Blocks created successfully")


if __name__ == "__main__":
    chunk_pages()
