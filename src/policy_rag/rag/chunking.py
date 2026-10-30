'''Documentation String'''
from typing import Dict,List
from policy_rag.rag.config import CHUNK_SIZE, CHUNK_OVERLAP
from policy_rag.rag.documents import POLICY_DOCUMENTS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_documents() -> List[Dict]:
    print("SECTION 1: DOCUMENT LOADING & CHUNKING")
    print("=" * 50)
    print(f"📄 Loaded {len(POLICY_DOCUMENTS)} policy documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n","\n"," ",""]
    )

    all_chunks=[]
    for doc in POLICY_DOCUMENTS:
        for i,chunk in enumerate(splitter.split_text(doc["content"]),1):
            all_chunks.append({
                "id": f"{doc['id']}_chunk_{i}",
                "title": doc["title"],
                "content": chunk,
                "category": doc["category"],
                "source_doc": doc["id"]
            })

    avg = sum(len(chunk["content"]) for chunk in all_chunks) // len(all_chunks)
    print(f"Created {len(all_chunks)} chunks from {len(POLICY_DOCUMENTS)} documents")
    print(f"Average chunk size: {avg} characters")

    #print(all_chunks)

    return all_chunks

#load_and_chunk_documents()
