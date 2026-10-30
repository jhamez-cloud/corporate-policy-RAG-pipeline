'''Documentation String'''
from policy_rag.rag.config import COLLECTION_NAME,SIMILARITY_METRIC
from policy_rag.rag.pipeline import build_index,run_rag_pipeline

TEST_QUERIES = [
    "What's the reimbursement policy for home office equipment?",
    "Can I get money back for buying a desk?",
    "How much can I claim for my home office?",
    "What's the travel expense policy?",
    "How many vacation days do I get?",
    "In the hidden of beyonders,humans must depend on a variety of potions, right?"
]

def main():
    print("PolicyCopilot - Complete RAG Pipeline Demo")
    print("=" * 60)

    collection = build_index()

    for i,query in enumerate(TEST_QUERIES,1):
        print(f"\nQuery-{i}: {query}")

        try:
            run_rag_pipeline(query,collection)
        except Exception as e:
            print(f"Error in demo {i}: {e}")


        if i < len(TEST_QUERIES):
            input("\nPress 'Enter' to move to next query... ")
    print("All Queries Completed!")

    print(f"Douments grouped into: {COLLECTION_NAME}\nPossible answers fetched by: {SIMILARITY_METRIC} meric.")

if __name__ == "__main__":
    main()
