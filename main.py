import os
import subprocess
from retrieval.fusion_qa import fusion_qa

# Files that must be cleared for single-PDF mode
RESET_FILES = [
    "storage/documents.db",
    "storage/knowledge_graph.db",
    "storage/vector_index.faiss",
    "storage/vector_meta.json",
    "storage/raw_pages.json",
    "storage/chunks.json"
]


def reset_storage():
    print("♻️ Resetting previous data (single PDF mode)...")
    for file in RESET_FILES:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Deleted {file}")


def ingest_pipeline():
    print("\n🚀 RUNNING INGESTION PIPELINE (SINGLE PDF MODE)\n")

    # 🔥 CLEAR OLD DATA FIRST
    reset_storage()

    # ✅ INGEST CURRENT PDF ONLY
    subprocess.run("python ingestion/read_pdf.py", shell=True)
    subprocess.run("python parsing/chunk_pages.py", shell=True)
    subprocess.run("python storage/store_sqlite.py", shell=True)
    subprocess.run("python storage/build_faiss_index.py", shell=True)
    subprocess.run("python kg/build_kg.py", shell=True)

    print("\n✅ Ingestion completed (old data cleared)\n")


def ask_question():
    print("\n📘 FUSION QA MODE (KG + Keyword + Vector)")
    print("Type 'exit' to return to main menu\n")

    while True:
        q = input("❓ Ask a question: ").strip()
        if q.lower() == "exit":
            break
        fusion_qa(q)


def main():
    while True:
        print("\n📚 RAG SYSTEM (NO LLM)")
        print("=" * 35)
        print("1. Re-ingest PDFs")
        print("2. Ask a question")
        print("3. Exit")

        choice = input("\nChoose (1/2/3): ").strip()

        if choice == "1":
            ingest_pipeline()
        elif choice == "2":
            ask_question()
        elif choice == "3":
            print("👋 Exiting system")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
