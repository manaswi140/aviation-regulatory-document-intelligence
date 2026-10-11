
from storage import (
    save_chunks,
    load_chunks,
    clear_saved_chunks,
)


def test_storage():
    sample_chunks = [
        {
            "document_name": "sample.pdf",
            "page_number": 1,
            "text": "This is a sample document passage.",
        }
    ]

    save_chunks(sample_chunks)
    loaded_chunks = load_chunks()

    assert loaded_chunks == sample_chunks
    print("PASS: Saved and loaded document chunks.")

    clear_saved_chunks()
    assert load_chunks() == []
    print("PASS: Saved chunks can be cleared.")

    print("\nAll storage tests passed!")


if __name__ == "__main__":
    test_storage()
