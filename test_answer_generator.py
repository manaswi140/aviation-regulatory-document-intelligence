
from answer_generator import generate_answer


def test_answer_generation():
    question = "What are the operations performed on files?"

    search_results = [
        {
            "document_name": "File_handling.pdf",
            "page_number": 3,
            "similarity_score": 0.67,
            "text": (
                "Operations on files include creating and opening "
                "a file, writing data in a file, traversing a file, "
                "and reading data from a file. "
                "On the other hand, binary files are made up of "
                "non-human readable characters and symbols."
            ),
        }
    ]

    result = generate_answer(question, search_results)

    assert result["answer"], "Answer should not be empty."
    assert "operations on files" in result["answer"].lower()
    assert "binary files" not in result["answer"].lower()
    assert result["sources"], "A source should be provided."
    assert result["sources"][0]["page_number"] == 3

    print("PASS: Answer is relevant and concise.")
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")

    for source in result["sources"]:
        print(
            f"{source['document_name']} "
            f"- Page {source['page_number']}"
        )


if __name__ == "__main__":
    test_answer_generation()
