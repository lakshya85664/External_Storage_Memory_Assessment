
import tempfile
from pathlib import Path

from memory_manager import MemoryManager
from memory_retriever import MemoryRetriever
from context_builder import ContextBuilder
from memory_summarizer import MemorySummarizer
from memory_vector_store import MemoryVectorStore


def main():
    print("=" * 60)
    print("EXTERNAL STORAGE MEMORY SYSTEM")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temporary_directory:
        base_path = Path(temporary_directory)

        memory_path = base_path / "memories.json"
        vector_path = base_path / "vectors.json"

        # 1. Initialize memory management.
        manager = MemoryManager(
            store_path=str(memory_path),
            short_term_limit=2
        )

        print("\n1. ADDING SHORT-TERM MEMORIES")

        manager.add_short_term("The user is learning Python.")
        manager.add_short_term("The user is studying AI agents.")
        manager.add_short_term("The user is building a memory system.")

        print("Short-term memories:")
        for memory in manager.get_short_term():
            print("-", memory)

        # 2. Inspect promoted long-term memories.
        long_term_memories = manager.get_long_term()

        print("\n2. LONG-TERM MEMORY")
        for memory in long_term_memories:
            print("-", memory["text"])

        # 3. Retrieve relevant memories.
        retriever = MemoryRetriever(
            store_path=str(memory_path)
        )

        print("\n3. MEMORY RETRIEVAL")

        retrieved = retriever.retrieve("learning Python")

        for memory in retrieved:
            print("-", memory["text"])

        # 4. Construct context.
        builder = ContextBuilder(
            store_path=str(memory_path)
        )

        print("\n4. CONTEXT CONSTRUCTION")
        print(builder.build("learning Python"))

        # 5. Summarize long-term memories.
        summarizer = MemorySummarizer()

        print("\n5. MEMORY SUMMARY")
        summary = summarizer.summarize(long_term_memories)
        print(summary)

        # 6. Index memories in the vector store.
        vector_store = MemoryVectorStore(vector_path)

        print("\n6. VECTOR INDEXING")

        for memory in long_term_memories:
            vector_store.add(memory)

        print("Indexed records:", len(vector_store.inspect()))

        # 7. Perform similarity search.
        print("\n7. VECTOR SIMILARITY SEARCH")

        results = vector_store.search("Python learning")

        for result in results:
            print(
                result["text"],
                "| Similarity:",
                round(result["score"], 4)
            )

        # 8. Simulate restarting the vector store.
        print("\n8. RESTART PERSISTENCE CHECK")

        restarted_store = MemoryVectorStore(vector_path)
        restart_results = restarted_store.search("Python learning")

        print("Records restored:", len(restarted_store.inspect()))
        print("Search results after restart:", len(restart_results))

        print("\n" + "=" * 60)
        print("MEMORY WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 60)


if __name__ == "__main__":
    main()
