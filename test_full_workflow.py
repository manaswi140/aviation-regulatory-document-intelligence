
from pathlib import Path

from document_pipeline import DocumentPipeline
from answer_generator import generate_answer


PDF_PATH = Path(
    r"C:\Users\Rishitha Nerella\Downloads\File_handling.pdf"
)


def test_full_workflow():
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    print("\nSTEP 1: Reading PDF...")
    pipeline = DocumentPipeline()

    chunks = pipeline.process_pdf(PDF_PATH)

    assert chunks, "No chunks were created."
    print(f"PASS: Created {len(chunks)} chunks.")

    print("\nSTEP 2: Building search index...")
    pipeline.build_search_index(chunks)

    assert pipeline.is_ready
    print("PASS: Search index is ready.")

    print("\nSTEP 3: Searching the document...")
    question = "What are the operations performed on files?"
    results = pipeline.search(question, top_k=3)

    assert results, "No search results returned."
    print(f"PASS: Retrieved {len(results)} passages.")

    print("\nSTEP 4: Generating the answer...")
    response = generate_answer(question, results)

    assert response["answer"], "Answer is empty."
    assert response["sources"], "No sources were returned."

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(response["answer"])

    print("\nSOURCES:")
    for source in response["sources"]:
        print(
            f"- {source['document_name']}, "
            f"page {source['page_number']}"
        )

    print("\nPASS: Full workflow completed successfully!")


if __name__ == "__main__":
    test_full_workflow()
