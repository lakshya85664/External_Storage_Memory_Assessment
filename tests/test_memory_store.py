
import json
import pytest

from memory_store import MemoryStore, new_memory


def test_save_and_load_memory(tmp_path):
    path = tmp_path / "memory.json"
    store = MemoryStore(path)

    record = new_memory("test_1", "Learning Python")
    store.save(record)

    loaded = MemoryStore(path).load_all()

    assert len(loaded) == 1
    assert loaded[0]["id"] == "test_1"
    assert loaded[0]["text"] == "Learning Python"


def test_duplicate_id_updates_existing_record(tmp_path):
    path = tmp_path / "memory.json"
    store = MemoryStore(path)

    store.save(new_memory("test_1", "First version"))
    store.save(new_memory("test_1", "Updated version"))

    records = store.load_all()

    assert len(records) == 1
    assert records[0]["text"] == "Updated version"


def test_missing_storage_returns_empty_list(tmp_path):
    store = MemoryStore(tmp_path / "missing.json")

    assert store.load_all() == []


def test_delete_memory(tmp_path):
    path = tmp_path / "memory.json"
    store = MemoryStore(path)

    store.save(new_memory("test_1", "Delete this memory"))
    store.delete("test_1")

    assert store.load_all() == []


def test_corrupted_json_is_rejected(tmp_path):
    path = tmp_path / "corrupted.json"
    path.write_text("{invalid json", encoding="utf-8")

    store = MemoryStore(path)

    with pytest.raises(RuntimeError):
        store.load_all()


def test_invalid_memory_type_is_rejected():
    with pytest.raises(ValueError):
        new_memory(
            "test_1",
            "Invalid memory",
            memory_type="temporary"
        )
