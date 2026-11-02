
from memory_manager import MemoryManager


def test_short_term_memory_limit(tmp_path):
    manager = MemoryManager(
        store_path=str(tmp_path / "memory.json"),
        short_term_limit=2
    )

    manager.add_short_term("First message")
    manager.add_short_term("Second message")
    manager.add_short_term("Third message")

    short_term = manager.get_short_term()
    long_term = manager.get_long_term()

    assert len(short_term) == 2
    assert len(long_term) == 1
    assert long_term[0]["text"] == "First message"


def test_short_term_promotion_is_persistent(tmp_path):
    path = tmp_path / "manager.json"

    manager = MemoryManager(
        store_path=str(path),
        short_term_limit=1
    )

    manager.add_short_term("First message")
    manager.add_short_term("Second message")

    reloaded = MemoryManager(
        store_path=str(path),
        short_term_limit=1
    )

    long_term = reloaded.get_long_term()

    assert len(long_term) == 1
    assert long_term[0]["text"] == "First message"


def test_add_long_term_memory(tmp_path):
    manager = MemoryManager(
        store_path=str(tmp_path / "memory.json")
    )

    manager.add_long_term(
        "manual_1",
        "Important project information"
    )

    records = manager.get_long_term()

    assert len(records) == 1
    assert records[0]["id"] == "manual_1"


def test_empty_manager(tmp_path):
    manager = MemoryManager(
        store_path=str(tmp_path / "empty.json")
    )

    assert manager.get_short_term() == []
    assert manager.get_long_term() == []
