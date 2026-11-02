
import pytest

from memory_vectorizer import MemoryVectorizer


def test_tokenize_text():
    vectorizer = MemoryVectorizer()

    tokens = vectorizer.tokenize("Python is Great!")

    assert tokens == ["python", "is", "great"]


def test_fit_creates_vocabulary():
    vectorizer = MemoryVectorizer()

    vectorizer.fit([
        "Python learning",
        "AI development"
    ])

    assert "python" in vectorizer.vocabulary
    assert "learning" in vectorizer.vocabulary
    assert "ai" in vectorizer.vocabulary


def test_transform_creates_correct_vector():
    vectorizer = MemoryVectorizer()

    vectorizer.fit([
        "Python learning",
        "AI development"
    ])

    vector = vectorizer.transform("Python learning")

    assert len(vector) == len(vectorizer.vocabulary)
    assert all(isinstance(value, (int, float)) for value in vector)


def test_fit_transform():
    vectorizer = MemoryVectorizer()

    vectors = vectorizer.fit_transform([
        "Python learning",
        "AI development"
    ])

    assert len(vectors) == 2
    assert len(vectors[0]) == len(vectors[1])


def test_cosine_similarity_identical_vectors():
    similarity = MemoryVectorizer.cosine_similarity(
        [1, 0, 1],
        [1, 0, 1]
    )

    assert similarity == pytest.approx(1.0)


def test_cosine_similarity_unrelated_vectors():
    similarity = MemoryVectorizer.cosine_similarity(
        [1, 0],
        [0, 1]
    )

    assert similarity == pytest.approx(0.0)


def test_cosine_similarity_rejects_mismatched_dimensions():
    with pytest.raises(ValueError):
        MemoryVectorizer.cosine_similarity(
            [1, 0],
            [1, 0, 1]
        )


def test_transform_requires_fitted_vocabulary():
    vectorizer = MemoryVectorizer()

    with pytest.raises(ValueError):
        vectorizer.transform("Python learning")
