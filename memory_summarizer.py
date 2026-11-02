
class MemorySummarizer:
    """Create compact summaries from stored memory records."""

    def summarize(self, memories, max_characters=200):
        if not isinstance(memories, list):
            raise TypeError("memories must be a list.")

        if not isinstance(max_characters, int) or isinstance(max_characters, bool):
            raise TypeError("max_characters must be an integer.")

        if max_characters <= 0:
            raise ValueError("max_characters must be positive.")

        if not memories:
            return ""

        texts = []

        for memory in memories:
            if not isinstance(memory, dict):
                raise ValueError("Each memory must be a dictionary.")

            text = memory.get("text")

            if not isinstance(text, str) or not text.strip():
                raise ValueError("Each memory must contain non-empty text.")

            texts.append(text.strip())

        summary = " ".join(texts)

        if len(summary) > max_characters:
            summary = summary[:max_characters].rsplit(" ", 1)[0]

        return summary


if __name__ == "__main__":
    from memory_store import MemoryStore

    store = MemoryStore("manager_memory.json")
    summarizer = MemorySummarizer()

    memories = store.load_all()
    summary = summarizer.summarize(memories, max_characters=200)

    print("Memory Summary:")
    print(summary)
    print("Summary characters:", len(summary))
