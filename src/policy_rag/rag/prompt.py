'''Documentation String'''
from typing import List,Dict
#from policy_rag.rag.retrieval import search_vector_database
#from policy_rag.rag.vector_store import setup_vector_database
#from policy_rag.rag.chunking import load_and_chunk_documents
#from policy_rag.rag.query import process_user_query

def augment_prompt_with_context(query:str, search_results: List[Dict]) -> str:
    print("\nSECTION 5: CONTEXT AUGMENTATION")
    print("=" * 50)

    context = "\n\n".join(
        f"Source {i}: {r['metadata']['title']}\n{r['content']}"
        for i,r in enumerate(search_results,1)
    )

    print(f"Assembled context from {len(search_results)} sources")
    print(f"Context length: {len(context)} characters")

    augmented_prompt = f"""
        Based on the following company policies, answer the user's question.

        POLICIES:
        {context}

        QUESTION: {query}

        Provide a clear, accurate answer based on the policies above.
        If the information is not available in the policies, say so.
        Include relevant policy details and any limitations or requirements.
    """

    print(f"Augmented prompt length: {len(augmented_prompt)} characters")
    print(f"Context sources: {[r['metadata']['title'] for r in search_results]}")

    print(f"\nAugmented Prompt: {augmented_prompt}")
    return augmented_prompt


#chunks = load_and_chunk_documents()
#collection = setup_vector_database(chunks)
#_,query_embeddings = process_user_query("When are Business travel expenses reimbursable?")
#search_results = search_vector_database(collection,query_embeddings)
#augment_prompt_with_context("business travel expense reimbursement",search_results)