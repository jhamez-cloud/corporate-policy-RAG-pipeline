'''Documentation String'''
from typing import List,Dict
import chromadb
from policy_rag.rag.config import COLLECTION_NAME,SIMILARITY_METRIC
#from policy_rag.rag.chunking import load_and_chunk_documents

def setup_vector_database(chunks: List[Dict]):
    print("\n🗄️ SECTION 2: VECTOR DATABASE SETUP")
    print("=" * 50)

    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name = COLLECTION_NAME,
        metadata={
            "hnsw:space": SIMILARITY_METRIC
        }
    )

    print(f"Vector DB Collection: {collection.name}")
    print(f"Similarity Metric Used: {SIMILARITY_METRIC}")

    if collection.count() == 0:
        collection.add(
            ids = [chunk["id"] for chunk in chunks],
            documents = [chunk["content"] for chunk in chunks],
            metadatas = [{
                "title":chunk["title"],"category":chunk["category"],"source":chunk["source_doc"]
            }for chunk in chunks]
        )

        print(f"Stored {len(chunks)} chunks in {collection.name} Vector Database...")
    else:
        print(f"{collection.name} Vector Database already contains {collection.count()} chunks")

    print(f"\nCollection Count: {collection.count()}")
    #print(collection.database())

    return collection

#chunked = load_and_chunk_documents()
#setup_vector_database(chunked)
