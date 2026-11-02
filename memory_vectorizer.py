
import math
import re
from collections import Counter


class MemoryVectorizer:
    """Convert memory text into Bag-of-Words numerical vectors."""

    def __init__(self):
        self.vocabulary = {}

    @staticmethod
    def tokenize(text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string.")

        return re.findall(r"\b[a-z0-9]+\b", text.lower())

    def fit(self, texts):
        if not isinstance(texts, list):
            raise TypeError("texts must be a list.")

        if not texts:
            raise ValueError("At least one text is required.")

        words = set()

        for text in texts:
            words.update(self.tokenize(text))

        self.vocabulary = {
            word: index
            for index, word in enumerate(sorted(words))
        }

        return self

    def transform(self, text):
        if not self.vocabulary:
            raise ValueError("Vectorizer has not been fitted.")

        tokens = self.tokenize(text)
        counts = Counter(tokens)

        return [
            float(counts.get(word, 0))
            for word in self.vocabulary
        ]

    def fit_transform(self, texts):
        self.fit(texts)

        return [
            self.transform(text)
            for text in texts
        ]

    @staticmethod
    def cosine_similarity(vector_a, vector_b):
        if len(vector_a) != len(vector_b):
            raise ValueError("Vectors must have equal dimensions.")

        dot_product = sum(
            a * b for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    texts = [
        "The user is learning Python.",
        "The user is studying AI agents."
    ]

    vectorizer = MemoryVectorizer()
    vectors = vectorizer.fit_transform(texts)

    print("Vocabulary:")
    print(vectorizer.vocabulary)

    print("\nGenerated vectors:")

    for text, vector in zip(texts, vectors):
        print(text)
        print(vector)

    similarity = vectorizer.cosine_similarity(
        vectors[0],
        vectors[1]
    )

    print("\nCosine similarity:", round(similarity, 4))
