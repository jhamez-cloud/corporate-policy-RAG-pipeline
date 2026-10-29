# Policy RAG

A small Retrieval-Augmented Generation (RAG) demo for answering employee questions about company policies (TechCorp PolicyCopilot). It chunks policy documents, stores them in ChromaDB, retrieves the most relevant chunks for a question, and builds an augmented prompt for an LLM.

The final generation step is **simulated** by default. Swap in a real LLM call in `generation.py` (see below).

## How it works

```
Documents → Chunking → Vector DB → Query embedding → Vector search → Prompt augmentation → Response
```

| Step | Module | What it does |
|------|--------|--------------|
| 1 | `chunking.py` | Splits policy documents into overlapping chunks |
| 2 | `vector_store.py` | Stores chunks in an in-memory ChromaDB collection (cosine similarity) |
| 3 | `query.py` | Cleans the question and embeds it with `all-MiniLM-L6-v2` |
| 4 | `retrieval.py` | Finds the top-k most similar chunks |
| 5 | `prompt.py` | Builds a prompt containing the retrieved context |
| 6 | `generation.py` | Generates the answer (simulated) |
| 7 | `pipeline.py` | Wires all steps together |

## Project structure

```
policy-rag/
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── policy_rag/
        ├── __init__.py
        ├── main.py          # entry point and demo queries
        ├── config.py        # chunk size, overlap, model, top_k, collection name
        ├── documents.py     # sample policy documents
        ├── chunking.py
        ├── vector_store.py
        ├── query.py
        ├── retrieval.py
        ├── prompt.py
        ├── generation.py
        └── pipeline.py
```

## Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/)

## Setup

### 1. Use CPU-only PyTorch

`sentence-transformers` depends on PyTorch. The default Linux build from PyPI is the CUDA version, which downloads several GB of NVIDIA packages. To avoid that, add this to `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
```

The marker limits the CPU index to Linux and Windows. On macOS the default torch is already CPU-only.

### 2. Install dependencies

Add `torch` **first** as a direct dependency. uv only applies `[tool.uv.sources]` to packages listed directly in the project, so torch must be added explicitly or it will resolve from PyPI.

```bash
uv add torch
```

Then add everything else:

```bash
uv add "scikit-learn==1.3.2" "rank-bm25==0.2.2" "pandas==2.1.4" "numpy>=1.26.0,<2" "matplotlib==3.7.2" "sentence-transformers==2.2.2" "huggingface_hub<0.26" "chromadb==0.4.22" "langchain==0.1.0" "spacy==3.7.2" mcp
```

### 3. Verify torch is CPU-only

```bash
grep -c nvidia uv.lock
```

This should print `0`.

### 4. Register the command

Add this to `pyproject.toml`:

```toml
[project.scripts]
policy-rag = "policy_rag.main:main"
```

Then sync:

```bash
uv sync
```

## Usage

```bash
uv run policy-rag
```

Or without the script entry:

```bash
uv run python -m policy_rag.main
```

The demo builds the index once, then runs five sample questions. Press Enter between questions.

## Configuration

All tunable values live in `src/policy_rag/config.py`:

| Setting | Default | Meaning |
|---------|---------|---------|
| `CHUNK_SIZE` | 200 | Maximum characters per chunk |
| `CHUNK_OVERLAP` | 50 | Characters shared between neighbouring chunks |
| `COLLECTION_NAME` | `techcorp_policies` | ChromaDB collection name |
| `SIMILARITY_METRIC` | `cosine` | Distance metric for the vector index |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `TOP_K` | 3 | Number of chunks retrieved per question |

## Using a real LLM

Replace the body of `generate_response` in `generation.py` with a call to your LLM of choice. It receives the fully built prompt (retrieved policies plus the question) and should return the answer as a string.

## Adding your own documents

Edit `POLICY_DOCUMENTS` in `documents.py`. Each document needs an `id`, `title`, `content`, and `category`. To load from files instead, replace that list with code that reads your files into the same structure.

## Troubleshooting

**Still downloading `nvidia-*` or `triton` packages.** Torch was not added as a direct dependency, or the `[tool.uv.sources]` block is missing or misplaced. Delete `.venv` and `uv.lock`, fix `pyproject.toml`, and repeat step 2.

**`cannot import name 'cached_download'`.** `sentence-transformers==2.2.2` is incompatible with newer `huggingface_hub`. The `huggingface_hub<0.26` pin fixes this.

**`No module named policy_rag`.** Run `uv sync` so the package is installed into the environment, and check that `pyproject.toml` has a `[build-system]` section.

**Dependency conflict between `langchain` and `chromadb`.** Loosen one pin, for example `chromadb>=0.4.22,<0.5`.

## Disk space

To reclaim space from earlier CUDA downloads:

```bash
uv cache prune
```