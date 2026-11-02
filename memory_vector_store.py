
import json
from pathlib import Path

from memory_vectorizer import MemoryVectorizer


class MemoryVectorStore:
    """Persist and retrieve vectorized long-term memories."""

    def __init__(self, path="memory_vectors.json"):
        self.path = Path(path)
        self.vectorizer = MemoryVectorizer()
        self.records = []
        self.load()

    
    def load(self):
        if not self.path.exists():
            self.records = []
            return

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Vector storage must contain a list.")

            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Invalid vector record.")

                if not {"id", "text", "vector"}.issubset(item):
                    raise ValueError("Vector record is missing fields.")

                if not isinstance(item["id"], str) or not item["id"].strip():
                    raise ValueError("Invalid vector ID.")

                if not isinstance(item["text"], str) or not item["text"].strip():
                    raise ValueError("Invalid vector text.")

                if not isinstance(item["vector"], list):
                    raise ValueError("Vector must be a list.")

                if not all(
                    isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    for value in item["vector"]
                ):
                    raise ValueError("Vector values must be numeric.")

            ids = [item["id"] for item in data]

            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate vector IDs detected.")

            self.records = data

            # Rebuild vocabulary after loading stored memories.
            if self.records:
                texts = [item["text"] for item in self.records]
                self.vectorizer.fit(texts)

                # Recalculate vectors using the restored vocabulary.
                for item in self.records:
                    item["vector"] = self.vectorizer.transform(
                        item["text"]
                    )

        except (json.JSONDecodeError, TypeError, KeyError) as error:
            raise ValueError("Vector storage is corrupted.") from error


    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        temporary_path = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4)

        temporary_path.replace(self.path)

    def add(self, memory):
        if not isinstance(memory, dict):
            raise TypeError("Memory must be a dictionary.")

        if memory.get("memory_type") != "long_term":
            raise ValueError("Only long-term memories can be indexed.")

        memory_id = memory.get("id")
        text = memory.get("text")

        if not isinstance(memory_id, str) or not memory_id.strip():
            raise ValueError("Memory ID must be non-empty.")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Memory text must be non-empty.")

        if any(item["id"] == memory_id for item in self.records):
            raise ValueError("Memory is already indexed.")

        normalized_text = " ".join(text.casefold().split())

        for item in self.records:
            existing_text = " ".join(
                item["text"].casefold().split()
            )

            if existing_text == normalized_text:
                raise ValueError("Duplicate memory content is not allowed.")

        if not self.vectorizer.vocabulary:
            self.vectorizer.fit([text])
        else:
            new_words = set(self.vectorizer.tokenize(text))
            missing_words = new_words - set(self.vectorizer.vocabulary)

            if missing_words:
                all_texts = [
                    item["text"] for item in self.records
                ] + [text]

                self.vectorizer.fit(all_texts)

                for item in self.records:
                    item["vector"] = self.vectorizer.transform(
                        item["text"]
                    )

        vector = self.vectorizer.transform(text)

        self.records.append({
            "id": memory_id,
            "text": text,
            "vector": vector
        })

        self.save()

    def search(self, query, top_k=5, min_similarity=0.0):
        if not isinstance(top_k, int) or isinstance(top_k, bool):
            raise TypeError("top_k must be an integer.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        if (
            not isinstance(min_similarity, (int, float))
            or isinstance(min_similarity, bool)
            or not 0 <= min_similarity <= 1
        ):
            raise ValueError("min_similarity must be between 0 and 1.")

        if not self.records:
            return []

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be non-empty.")

        query_words = set(self.vectorizer.tokenize(query))
        vocabulary_words = set(self.vectorizer.vocabulary)

        if not query_words.intersection(vocabulary_words):
            return []

        query_vector = self.vectorizer.transform(query)

        results = []

        for item in self.records:
            score = self.vectorizer.cosine_similarity(
                query_vector,
                item["vector"]
            )

            if score >= min_similarity and score > 0:
                results.append({
                    "id": item["id"],
                    "text": item["text"],
                    "score": score
                })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]

    def inspect(self):
        return self.records


if __name__ == "__main__":
    from memory_store import MemoryStore

    memory_store = MemoryStore("manager_memory.json")
    vector_store = MemoryVectorStore("memory_vectors.json")

    for memory in memory_store.load_all():
        if not any(
            item["id"] == memory["id"]
            for item in vector_store.records
        ):
            vector_store.add(memory)

    print("Indexed memories:")

    for item in vector_store.inspect():
        print("ID:", item["id"])
        print("Text:", item["text"])
        print("Vector:", item["vector"])

    print("\nSimilarity search:")

    results = vector_store.search("learning Python")

    for result in results:
        print(
            result["text"],
            "| Similarity:",
            round(result["score"], 4)
        )
