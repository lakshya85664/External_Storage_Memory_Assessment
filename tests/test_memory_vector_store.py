
import pytest

from memory_vector_store import MemoryVectorStore


def create_memory(memory_id, text):
    return {
        "id": memory_id,
        "text": text,
        "memory_type": "long_term",
        "metadata": {}
    }


def test_add_and_inspect_memory(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    store.add(create_memory("m1", "The user is learning Python"))

    records = store.inspect()

    assert len(records) == 1
    assert records[0]["id"] == "m1"


def test_similarity_search_finds_relevant_memory(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    store.add(create_memory("m1", "The user is learning Python"))
    store.add(create_memory("m2", "The user enjoys gardening"))

    results = store.search("learning Python")

    assert len(results) >= 1
    assert results[0]["id"] == "m1"


def test_duplicate_memory_id_is_rejected(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    store.add(create_memory("m1", "Learning Python"))

    with pytest.raises(ValueError):
        store.add(create_memory("m1", "Learning Java"))


def test_short_term_memory_is_rejected(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    memory = create_memory("m1", "Temporary message")
    memory["memory_type"] = "short_term"

    with pytest.raises(ValueError):
        store.add(memory)


def test_empty_vector_store_returns_no_results(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    assert store.search("Python") == []


def test_search_after_restart(tmp_path):
    path = tmp_path / "vectors.json"

    first_store = MemoryVectorStore(path)
    first_store.add(
        create_memory("m1", "The user is learning Python")
    )
    first_store.add(
        create_memory("m2", "The user enjoys gardening")
    )

    # Simulate restarting the application.
    restarted_store = MemoryVectorStore(path)
    results = restarted_store.search("learning Python")

    assert len(results) >= 1
    assert results[0]["id"] == "m1"


def test_duplicate_memory_content_is_rejected(tmp_path):
    store = MemoryVectorStore(tmp_path / "vectors.json")

    store.add(
        create_memory("m1", "The user is learning Python")
    )

    with pytest.raises(ValueError):
        store.add(
            create_memory("m2", "  the USER is learning python  ")
        )
