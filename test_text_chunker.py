
from text_chunker import chunk_pages


def test_chunking_and_metadata():
    pages = [
        {
            "page_number": 4,
            "text": "A" * 1200,
        },
        {
            "page_number": 5,
            "text": "B" * 400,
        },
    ]

    chunks = chunk_pages(
        pages,
        document_name="sample_regulation.pdf",
        chunk_size=1000,
        overlap=150,
    )

    assert len(chunks) == 3
    assert chunks[0]["page_number"] == 4
    assert chunks[1]["page_number"] == 4
    assert chunks[2]["page_number"] == 5

    assert chunks[0]["document_name"] == "sample_regulation.pdf"
    assert len(chunks[0]["text"]) == 1000
    assert len(chunks[1]["text"]) == 350
    assert len(chunks[2]["text"]) == 400

    assert chunks[0]["text"][-150:] == chunks[1]["text"][:150]

    print("PASS: Chunking, overlap, and source metadata work.")


if __name__ == "__main__":
    test_chunking_and_metadata()