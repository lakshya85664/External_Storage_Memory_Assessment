
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import os


@dataclass
class Memory:
    id: str
    text: str
    memory_type: str
    timestamp: str
    metadata: dict

    def to_dict(self):
        return asdict(self)


def new_memory(memory_id, text, memory_type="long_term", metadata=None):
    """Create a memory record with a UTC timestamp."""

    if not isinstance(memory_id, str) or not memory_id.strip():
        raise ValueError("Memory ID must be non-empty.")

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Memory text must be non-empty.")

    if memory_type not in ("short_term", "long_term"):
        raise ValueError("Invalid memory type.")

    if metadata is not None and not isinstance(metadata, dict):
        raise TypeError("Metadata must be a dictionary.")

    return Memory(
        id=memory_id,
        text=text,
        memory_type=memory_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        metadata=metadata or {}
    )


class MemoryStore:
    """Persistent JSON-backed external memory storage."""

    def __init__(self, path="memory.json"):
        self.path = Path(path)

    def _read(self):
        """Read stored records safely."""

        if not self.path.exists():
            return []

        try:
            data = json.loads(
                self.path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RuntimeError(
                "Storage file is not valid JSON."
            ) from exc

        if not isinstance(data, list):
            raise RuntimeError(
                "Storage file must contain a JSON list."
            )

        return data

    def _write(self, records):
        """Write records atomically using a temporary file."""

        self.path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        try:
            temp_path.write_text(
                json.dumps(
                    records,
                    indent=2,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            os.replace(temp_path, self.path)

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def save(self, record):
        """Save a memory. Existing IDs are updated."""

        if isinstance(record, Memory):
            record = record.to_dict()

        if not isinstance(record, dict):
            raise TypeError("Record must be a Memory or dictionary.")

        required = {
            "id", "text", "memory_type", "timestamp", "metadata"
        }

        if not required.issubset(record):
            raise ValueError("Memory record is missing required fields.")

        if not all(
            isinstance(record[field], str) and record[field].strip()
            for field in ("id", "text", "memory_type", "timestamp")
        ):
            raise ValueError("Memory fields must contain non-empty text.")

        if record["memory_type"] not in ("short_term", "long_term"):
            raise ValueError("Invalid memory type.")

        if not isinstance(record["metadata"], dict):
            raise TypeError("Metadata must be a dictionary.")

        records = self._read()

        # Improvement: update by ID instead of creating duplicates.
        records = [
            item for item in records
            if item.get("id") != record["id"]
        ]

        records.append(record)
        self._write(records)

    def load_all(self):
        """Load every persisted memory record."""
        return self._read()

    def delete(self, memory_id):
        """Delete a memory using its ID."""

        records = self._read()

        updated = [
            record for record in records
            if record.get("id") != memory_id
        ]

        self._write(updated)


if __name__ == "__main__":
    store = MemoryStore("memory.json")

    memory = new_memory(
        memory_id="m1",
        text="Learner prefers Python examples.",
        memory_type="long_term",
        metadata={"source": "profile"}
    )

    store.save(memory)

    print("Saved memory:")
    print(memory.to_dict())

    print("\nAll stored memories:")
    print(json.dumps(store.load_all(), indent=2))
