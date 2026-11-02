
import pytest

from memory_summarizer import MemorySummarizer


def test_summarize_multiple_memories():
    memories = [
        {"text": "The user is learning Python."},
        {"text": "The user is studying AI agents."},
    ]

    summarizer = MemorySummarizer()
    summary = summarizer.summarize(memories)

    assert "learning Python" in summary
    assert "AI agents" in summary


def test_summary_respects_character_limit():
    memories = [
        {"text": "Python is a programming language."},
        {"text": "It is widely used in AI development."},
    ]

    summarizer = MemorySummarizer()
    summary = summarizer.summarize(
        memories,
        max_characters=20
    )

    assert len(summary) <= 20


def test_empty_memory_list():
    summarizer = MemorySummarizer()

    assert summarizer.summarize([]) == ""


def test_invalid_character_limit():
    summarizer = MemorySummarizer()

    with pytest.raises(ValueError):
        summarizer.summarize(
            [{"text": "Python"}],
            max_characters=0
        )


def test_invalid_memory_record():
    summarizer = MemorySummarizer()

    with pytest.raises(ValueError):
        summarizer.summarize(
            [{"text": ""}]
        )
