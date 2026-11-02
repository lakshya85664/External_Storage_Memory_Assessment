
from memory_store import MemoryStore, new_memory


class MemoryManager:
    """Manages short-term and persistent long-term memory."""

    def __init__(self, store_path="memory.json", short_term_limit=3):
        if not isinstance(short_term_limit, int) or isinstance(short_term_limit, bool):
            raise TypeError("short_term_limit must be an integer.")

        if short_term_limit <= 0:
            raise ValueError("short_term_limit must be positive.")

        self.store = MemoryStore(store_path)
        self.short_term_limit = short_term_limit
        self.short_term = []

    def add_short_term(self, text):
        """Add a recent message and promote overflow to long-term memory."""

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Message must be non-empty.")

        self.short_term.append(text)

        if len(self.short_term) > self.short_term_limit:
            oldest = self.short_term.pop(0)

            memory_id = f"auto_{len(self.store.load_all()) + 1}"

            record = new_memory(
                memory_id=memory_id,
                text=oldest,
                memory_type="long_term",
                metadata={"source": "short_term_promotion"}
            )

            self.store.save(record)

    def add_long_term(self, memory_id, text, metadata=None):
        """Save important information directly to persistent memory."""

        record = new_memory(
            memory_id=memory_id,
            text=text,
            memory_type="long_term",
            metadata=metadata
        )

        self.store.save(record)

    def get_short_term(self):
        return list(self.short_term)

    def get_long_term(self):
        return self.store.load_all()

    def inspect(self):
        """Display both memory layers."""

        print("\n=== SHORT-TERM MEMORY ===")

        for item in self.short_term:
            print("-", item)

        print("\n=== LONG-TERM MEMORY ===")

        for item in self.get_long_term():
            print(
                item["id"],
                "|",
                item["memory_type"],
                "|",
                item["text"]
            )


if __name__ == "__main__":
    manager = MemoryManager(
        store_path="manager_memory.json",
        short_term_limit=3
    )

    manager.add_short_term("The user is learning Python.")
    manager.add_short_term("The user is studying AI agents.")
    manager.add_short_term("The user prefers practical examples.")

    print("After adding three messages:")
    manager.inspect()

    manager.add_short_term("The user is working on memory systems.")

    print("\nAfter adding a fourth message:")
    manager.inspect()
