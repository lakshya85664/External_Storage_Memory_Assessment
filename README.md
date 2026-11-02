# External Storage Memory Assessment

## Project overview

This project implements a persistent external-memory layer for an AI agent. It separates short-term working memory from long-term stored memories, retrieves relevant information, constructs context for later reasoning, summarizes stored information, and provides a lightweight vector-based similarity search.

The implementation uses Python's standard library for storage and vectorization. `pytest` is used for automated testing.

## Learning objectives and implementation

- **External storage:** `memory_store.py` stores memory records in JSON, supports loading, saving, updating by ID, and deletion.
- **Memory lifecycle:** `memory_manager.py` maintains a bounded short-term buffer and promotes the oldest entry to long-term storage when the configured limit is exceeded.
- **Retrieval:** `memory_retriever.py` ranks long-term memories using keyword overlap. `context_builder.py` formats retrieved memories into context.
- **Summarization:** `memory_summarizer.py` combines memory text and enforces a configurable character limit.
- **Vector extension:** `memory_vectorizer.py` creates Bag-of-Words vectors and calculates cosine similarity. `memory_vector_store.py` persists indexed long-term memories and searches them by similarity.
- **Integration:** `main.py` demonstrates the end-to-end workflow, including a vector-store restart check.

## Project structure

```text
External_Storage_Memory_Assessment/
├── context_builder.py
├── main.py
├── memory_manager.py
├── memory_retriever.py
├── memory_store.py
├── memory_summarizer.py
├── memory_vector_store.py
├── memory_vectorizer.py
├── requirements.txt
├── .gitignore
└── tests/
    ├── test_memory_manager.py
    ├── test_memory_store.py
    ├── test_memory_summarizer.py
    ├── test_memory_vector_store.py
    ├── test_memory_vectorizer.py
    └── test_retrieval.py
```

Runtime JSON files are generated locally and excluded from Git using `.gitignore`.

## Setup and execution (Windows CMD)

```cmd
cd /d E:\Tayana_Projects\Memory_Engineering\External_Storage_Memory_Assessment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Run the automated test suite:

```cmd
python -m pytest -v
```

**Verified result:** 35 tests passed.

## Reliability improvements

1. **Vocabulary restoration after restart:** the vector store rebuilds its vocabulary from persisted memory text and recalculates vectors when it loads. This keeps similarity search functional after a new `MemoryVectorStore` instance is created.
2. **Duplicate-content prevention:** vector indexing rejects memory text that duplicates existing content after case-folding and whitespace normalization, even if the incoming record has a different ID.

Additional safeguards include JSON validation, atomic writes, duplicate-ID handling, input validation, and explicit handling of missing or corrupted storage.

## Reflection (approximately 300 words)

Building this external storage memory system helped me understand why an agent needs more than a language model's immediate context window. A model can reason over the information supplied to one request, but an application needs a separate mechanism to retain useful information across interactions and application restarts. Implementing JSON-backed storage made persistence concrete: records had to be validated, written safely, loaded again, and handled when the file was missing or corrupted.

The memory manager helped me distinguish short-term working memory from long-term memory. Limiting the short-term buffer and promoting the oldest item showed how a simple memory lifecycle can be implemented without allowing the working buffer to grow indefinitely. I then connected storage to retrieval and context construction. This demonstrated that storing everything is not enough; an agent must select relevant information and present it in a useful format for the next reasoning step.

The summarization and vectorization exercises introduced two different ways to reduce or search memory. The summarizer creates a compact text representation, while the Bag-of-Words vectorizer represents text numerically so cosine similarity can rank related records. The vector approach is intentionally lightweight and is not a semantic embedding model, but it provided a practical way to understand indexing and similarity search.

Testing exposed an important restart defect: the stored vectors alone were insufficient because the vocabulary used to create them was not restored. Rebuilding the vocabulary and recalculating vectors on load made the vector store usable across sessions. I also added normalized duplicate-content detection to prevent the same information from being indexed under different IDs.

The most valuable lesson was that memory engineering involves reliability as much as retrieval logic. Persistence, validation, restart behavior, duplicate handling, and isolated tests all contribute to a dependable agent memory component.
