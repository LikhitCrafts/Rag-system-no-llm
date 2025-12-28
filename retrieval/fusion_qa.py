from retrieval.kg_qa import kg_fact_lookup
from retrieval.keyword_search import search_blocks


def fusion_qa(question):
    print("\n🧠 FUSION QA SYSTEM")
    print("────────────────────────────")
    print("⏳ Processing your question...\n")

    print("🔗 Checking Knowledge Graph...")
    kg = kg_fact_lookup(question)
    if kg:
        print("\n✅ Answer Source: Knowledge Graph\n")
        for a in kg:
            print("•", a)
        return

    print("🔍 Searching document keywords...")
    results = search_blocks(question)

    if results:
        print("\n✅ Answer Source: Keyword Search\n")
        for score, page, text in results:
            print(f"[Page {page}] (score={score})")
            print(text[:700])
            print("-" * 60)
        return

    print("\n❌ NO ANSWER FOUND")
    print("ℹ️ The document does not contain this information.")
