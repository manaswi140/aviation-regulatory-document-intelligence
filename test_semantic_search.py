
from semantic_search import SemanticSearch


def test_semantic_search():
    chunks = [
        {
            "chunk_id": 1,
            "document_name": "regulations.pdf",
            "page_number": 4,
            "text": (
                "Aircraft maintenance must be performed "
                "according to the approved maintenance programme."
            ),
        },
        {
            "chunk_id": 2,
            "document_name": "regulations.pdf",
            "page_number": 7,
            "text": (
                "Flight crew members must receive appropriate "
                "training before performing assigned duties."
            ),
        },
        {
            "chunk_id": 3,
            "document_name": "regulations.pdf",
            "page_number": 9,
            "text": (
                "Aircraft certification requires compliance "
                "with applicable airworthiness requirements."
            ),
        },
    ]

    search_engine = SemanticSearch()
    search_engine.build_index(chunks)

    results = search_engine.search(
        "What rules apply to aircraft maintenance?",
        top_k=2,
    )

    assert len(results) == 2
    assert all("page_number" in result for result in results)
    assert all("similarity_score" in result for result in results)

    print("PASS: Semantic search returned ranked passages.")
    print("\nRetrieved passages:")

    for result in results:
        print(
            f"Page {result['page_number']} | "
            f"Score: {result['similarity_score']:.3f}"
        )
        print(result["text"])
        print()


if __name__ == "__main__":
    test_semantic_search()