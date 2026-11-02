
from memory_store import MemoryStore, new_memory
from memory_retriever import MemoryRetriever
from context_builder import ContextBuilder


def create_test_store(path):
    store = MemoryStore(path)

    store.save(new_memory("m1", "The user is learning Python"))
    store.save(new_memory("m2", "The user is studying machine learning"))
    store.save(new_memory("m3", "The user enjoys backend development"))

    return store


def test_retrieve_relevant_memories(tmp_path):
    path = tmp_path / "memory.json"
    create_test_store(path)

    retriever = MemoryRetriever(store_path=str(path))
    results = retriever.retrieve("Python learning")

    assert len(results) >= 1
    assert results[0]["id"] == "m1"


def test_retrieval_respects_top_k(tmp_path):
    path = tmp_path / "memory.json"
    create_test_store(path)

    retriever = MemoryRetriever(store_path=str(path))
    results = retriever.retrieve("user", top_k=2)

    assert len(results) == 2


def test_unrelated_query_returns_no_results(tmp_path):
    path = tmp_path / "memory.json"
    create_test_store(path)

    retriever = MemoryRetriever(store_path=str(path))
    results = retriever.retrieve("astronomy galaxies")

    assert results == []


def test_context_builder_constructs_context(tmp_path):
    path = tmp_path / "memory.json"
    create_test_store(path)

    builder = ContextBuilder(
        store_path=str(path)
    )
    context = builder.build("Python")

    assert "Relevant information" in context
    assert "learning Python" in context


def test_context_builder_handles_no_results(tmp_path):
    path = tmp_path / "memory.json"
    create_test_store(path)

    builder = ContextBuilder(
        store_path=str(path)
    )
    context = builder.build("astronomy galaxies")

    assert context == "No relevant memories found."
