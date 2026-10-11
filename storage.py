
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CHUNKS_FILE = DATA_DIR / "processed_chunks.json"


def save_chunks(chunks):
    """Save processed document chunks to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with CHUNKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)


def load_chunks():
    """Load previously saved chunks."""
    if not CHUNKS_FILE.exists():
        return []

    try:
        with CHUNKS_FILE.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        if not isinstance(chunks, list):
            raise ValueError("Saved chunks must be a list.")

        return chunks

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            f"Could not load saved document chunks: {error}"
        ) from error


def clear_saved_chunks():
    """Delete the saved chunk file."""
    if CHUNKS_FILE.exists():
        CHUNKS_FILE.unlink()
