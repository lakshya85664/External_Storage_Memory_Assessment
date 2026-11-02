
from memory_retriever import MemoryRetriever


class ContextBuilder:
    """Build an LLM-ready context from retrieved memories."""

    def __init__(self, store_path="memory.json", top_k=5):
        self.retriever = MemoryRetriever(store_path)
        self.top_k = top_k

    def build(self, query):
        """Retrieve relevant memories and construct context."""

        memories = self.retriever.retrieve(
            query=query,
            top_k=self.top_k
        )

        if not memories:
            return "No relevant memories found."

        context_lines = [
            "Relevant information from long-term memory:"
        ]

        for index, memory in enumerate(memories, start=1):
            context_lines.append(
                f"{index}. {memory['text']}"
            )

        return "\n".join(context_lines)


if __name__ == "__main__":
    builder = ContextBuilder(
        store_path="manager_memory.json",
        top_k=5
    )

    context = builder.build("learning Python")

    print("Constructed Context:")
    print(context)
