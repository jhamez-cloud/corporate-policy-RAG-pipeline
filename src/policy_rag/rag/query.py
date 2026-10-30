'''Documentation String'''
from policy_rag.rag.config import EMBEDDING_MODEL
from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_embedding_model()->SentenceTransformer:
    """Load Embedding Model Once , Reuse for every query"""
    return SentenceTransformer(EMBEDDING_MODEL)

def process_user_query(query:str):
    print("\nSECTION 3: QUERY PROCESSING")
    print("=" * 50)

    model = get_embedding_model()
    print(f"Using Model: {EMBEDDING_MODEL}")
    print(f"Embedding Diimensions: {model.get_sentence_embedding_dimension()}")

    cleaned_query = query.lower().strip()
    print(f"\nOriginal Query: {query}")
    print(f"Cleaned Query: {cleaned_query}")

    query_embedding = model.encode([cleaned_query])
    print(f"Query Embedding Shape: {query_embedding.shape}")
    print(f"Embedding Sample: {query_embedding[0][:5]}...")

    return model,query_embedding[0]


#process_user_query("What's the reimbursement policy FOR home ofFice equiPment?   ")