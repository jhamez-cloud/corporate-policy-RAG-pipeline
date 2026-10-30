from policy_rag.rag.chunking import load_and_chunk_documents
from policy_rag.rag.vector_store import setup_vector_database
from policy_rag.rag.query import process_user_query
from policy_rag.rag.retrieval import search_vector_database
from policy_rag.rag.prompt import augment_prompt_with_context
from policy_rag.rag.generation import generate_response

def build_index():
    """Load Documents, Chunk Documents, Create Vector DB Collection"""
    chunks = load_and_chunk_documents()
    collection = setup_vector_database(chunks)

    return collection

def run_rag_pipeline(query:str, collection = None) -> str :
    """Running Pipeline: Retrieval[Prompt process],Augment[Prompt + Context Augment],Generate"""
    print("\n🚀 COMPLETE RAG PIPELINE DEMO")
    print(f"User Question: {query}")
    print("=" * 60)

    if collection is None:
        collection = build_index()

    _,query_embeddings = process_user_query(query)
    search_results = search_vector_database(collection,query_embeddings)
    augmented_prompt = augment_prompt_with_context(query,search_results)
    response = generate_response(augmented_prompt)

    print("\n🎉 FINAL RESULT")
    print("=" * 60)
    print(response)
    print("=" * 60)

    return response


# rag_pipeline("When are Business travel expenses reimbursable?")