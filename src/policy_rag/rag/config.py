'''Documentation String'''
from pathlib import Path

#documents / dataset
DATA_DIR = Path(__file__).resolve().parents[3] / "policy-docs"

#chunking
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

#vector database
COLLECTION_NAME = "corporate_policies"
SIMILARITY_METRIC = "cosine"

#embedding
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

#retrieval
TOP_K = 3

#llm model
LLM_MODEL = "gemini-3.8-flash"
LLM_MAX_TOKENS = 1000