 RAG System (No LLM)

This project is a **Retrieval-Augmented Generation (RAG) system without using any Large Language Model (LLM)**.
It answers questions strictly based on the content present in the provided PDF documents.

The system supports **dynamic ingestion of any single PDF** and avoids hallucinations by returning answers
only when information is explicitly available in the document.

---

Features

- Works with **any single PDF**
- No LLMs used (pure retrieval-based system)
- Knowledge Graph–based factual answering
- Keyword-based document search
- Vector similarity search using FAISS
- Safe answers (returns *No Answer Found* if content is missing)
- Re-ingestion clears old data automatically

---

Project Structure

Rag-system/
│── data/
│ └── pdfs/ # Input PDFs
│
│── ingestion/ # PDF reading & text extraction
│── parsing/ # Chunking logic
│── storage/ # SQLite, FAISS, and KG storage
│── retrieval/ # KG, keyword, and vector QA logic
│── kg/ # Knowledge graph construction
│
│── main.py # Entry point
│── README.md
│── .gitignore


---

How It Works

1. **Ingestion**
   - Reads the PDF
   - Extracts text
   - Splits into blocks
   - Stores blocks in SQLite
   - Builds FAISS vector index
   - Builds a clean Knowledge Graph

2. **Question Answering**
   - Tries Knowledge Graph first
   - Falls back to keyword search
   - Then vector similarity search
   - If nothing matches → returns *No Answer Found*

---
requirements
 
1. pymupdf
2. faiss-cpu
3. numpy
4. tqdm
py -m venv venv
py -m pip install --upgrade pip
pip install pymupdf faiss-cpu numpy tqdm
python -c "import fitz, faiss; print('ALL OK')"

-----

 How to Run

```bash
python main.py

1 → Re-ingest PDF

2 → Ask questions

3 → ExiT


Notes

This system does not generate answers
It only retrieves evidence from documents
Ideal for academic, legal, and compliance use cases

Future Improvements

Add LLM-based summarization (optional)
Support multiple PDFs
Improve entity extraction for unstructured text
Add UI (Streamlit / Web app)
Add OCL Tech


