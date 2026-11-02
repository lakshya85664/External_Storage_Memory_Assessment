
from memory_store import MemoryStore


class MemoryRetriever:
    """Retrieve relevant memories from persistent storage."""

    def __init__(self, store_path="memory.json"):
        self.store = MemoryStore(store_path)

    def retrieve(self, query, top_k=5):
        """Return the most relevant memories using keyword matching."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        if not isinstance(top_k, int) or isinstance(top_k, bool):
            raise TypeError("top_k must be an integer.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        memories = self.store.load_all()
        query_words = set(query.lower().split())

        scored_memories = []

        for memory in memories:
            text = memory.get("text", "").lower()
            memory_words = set(text.split())

            score = len(query_words.intersection(memory_words))

            if score > 0:
                scored_memories.append((score, memory))

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            memory
            for score, memory in scored_memories[:top_k]
        ]


if __name__ == "__main__":
    retriever = MemoryRetriever("manager_memory.json")

    results = retriever.retrieve("learning Python")

    print("Retrieved memories:")

    for memory in results:
        print("-", memory["text"])
