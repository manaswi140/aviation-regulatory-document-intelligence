
from answer_generator import generate_answer


TEST_CASES = [
    {
        "question": "What are the operations performed on files?",
        "passage": (
            "But operations on files include creating and opening "
            "a file, writing data in a file, traversing a file, "
            "reading data from a file and so on. "
            "There are mainly two types of data files: text file "
            "and binary file."
        ),
        "expected": "operations on files include",
        "unwanted": "binary file",
        "page": 3,
    },
    {
        "question": "How do you open a file in Python?",
        "passage": (
            "2.3.1 Opening a file To open a file in Python, "
            "we use the open() function. "
            "The syntax of open() is as follows: "
            "file_object = open(file_name, access_mode). "
            "Binary files are made up of non-human readable symbols."
        ),
        "expected": "open()",
        "unwanted": "binary files",
        "page": 3,
    },
    {
        "question": "What is a file object?",
        "passage": (
            "This function returns a file object called file handle "
            "which is stored in the variable file_object. "
            "We can use this variable to transfer data to and from "
            "the file. Binary files contain non-human readable data."
        ),
        "expected": "file object",
        "unwanted": "binary files",
        "page": 3,
    },
]


def test_answer_quality():
    for case in TEST_CASES:
        results = [{
            "document_name": "File_handling.pdf",
            "page_number": case["page"],
            "text": case["passage"],
            "similarity_score": 0.8,
        }]

        response = generate_answer(
            case["question"],
            results,
        )

        answer = response["answer"].lower()

        assert case["expected"] in answer, (
            f"Expected phrase not found for: {case['question']}\n"
            f"Answer: {response['answer']}"
        )

        assert case["unwanted"] not in answer, (
            f"Unrelated content found for: {case['question']}\n"
            f"Answer: {response['answer']}"
        )

        assert response["sources"], "Source reference is missing."
        assert response["sources"][0]["page_number"] == case["page"]

        print(f"\nPASS: {case['question']}")
        print(f"Answer: {response['answer']}")
        print(
            f"Source: {response['sources'][0]['document_name']}, "
            f"page {response['sources'][0]['page_number']}"
        )

    print("\nAll answer-quality tests passed!")


if __name__ == "__main__":
    test_answer_quality()

