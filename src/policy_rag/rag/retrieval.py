'''Documentation String'''
from policy_rag.rag.config import TOP_K
from typing import List,Dict
#from policy_rag.rag.chunking import load_and_chunk_documents
#from policy_rag.rag.vector_store import setup_vector_database
#from policy_rag.rag.query import process_user_query

def search_vector_database(collection,query_embedding,top_k : int = TOP_K)-> List[Dict]:
    print("\nSECTION 4: VECTOR SEARCH")
    print("=" * 50)

    results = collection.query(
        query_embeddings = [query_embedding.tolist()],
        n_results = top_k
    )
    print(f"\nSearching for top: {top_k} results...")
    print(f"Found {len(results['ids'][0])} relevant chunks")

    search_results = []
    for i,(doc_id,distance,content,metadata) in enumerate(zip(
        results["ids"][0],
        results["distances"][0],
        results["documents"][0],
        results["metadatas"][0],
    )):
        similarity = 1 - distance
        search_results.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata,
            "similarity":  similarity,
        })

        print(f"\n{i + 1}.{metadata['title']} (Category: {metadata['category']})")
        print(f"   Similarity: {similarity:.3f}")
        print(f"   Content: {content[:100]}...")

    return search_results


#chunks = load_and_chunk_documents()
#collection = setup_vector_database(chunks)
#_,query_embedding = process_user_query("When are Business travel expenses reimbursable?")
#search_vector_database(collection,query_embedding)

