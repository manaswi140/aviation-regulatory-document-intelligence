
import io
import pymupdf

from document_pipeline import DocumentPipeline


def create_test_pdf():
    """Create a small PDF in memory for testing."""
    pdf = pymupdf.open()

    page1 = pdf.new_page()
    page1.insert_text(
        (72, 72),
        "Aircraft maintenance must follow approved procedures."
    )

    page2 = pdf.new_page()
    page2.insert_text(
        (72, 72),
        "Personnel must complete required safety training."
    )

    pdf_bytes = pdf.tobytes()
    pdf.close()

    uploaded_file = io.BytesIO(pdf_bytes)
    uploaded_file.name = "test_regulatory_document.pdf"

    return uploaded_file


def main():
    pipeline = DocumentPipeline()

    test_pdf = create_test_pdf()

    # Test PDF extraction and chunking
    chunks = pipeline.process_pdf(test_pdf)

    assert len(chunks) == 2, (
        f"Expected 2 chunks, but received {len(chunks)}"
    )

    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2

    assert "maintenance" in chunks[0]["text"].lower()
    assert "safety training" in chunks[1]["text"].lower()

    assert chunks[0]["document_name"] == "test_regulatory_document.pdf"

    print("PASS: PDF processing and chunking work correctly.")
    print(f"Chunks created: {len(chunks)}")

    # Test semantic indexing and search
    pipeline.build_search_index(chunks)

    results = pipeline.search(
        "What is required for aircraft maintenance?",
        top_k=2
    )

    assert len(results) > 0, "Search returned no results."

    assert "maintenance" in results[0]["text"].lower(), (
        "The most relevant result was not the maintenance passage."
    )

    assert "similarity_score" in results[0]

    print("PASS: Semantic indexing and search work correctly.")
    print("\nTop search result:")
    print(f"Document: {results[0]['document_name']}")
    print(f"Page: {results[0]['page_number']}")
    print(f"Text: {results[0]['text']}")
    print(f"Similarity score: {results[0]['similarity_score']:.3f}")
    print("\nALL TESTS PASSED!")


if __name__ == "__main__":
    main()