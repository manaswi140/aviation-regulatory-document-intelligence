
from pathlib import Path

from pdf_processor import extract_text_from_pdf
from text_chunker import chunk_pages


PDF_PATH = Path("C:/Users/Rishitha Nerella/Downloads/File_handling.pdf")


def main():
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH.resolve()}")
        print("Place File_handling.pdf in your project folder.")
        return

    pages = extract_text_from_pdf(str(PDF_PATH))

    chunks = chunk_pages(
        pages,
        document_name=PDF_PATH.name,
        chunk_size=500,
        overlap=80,
    )

    print(f"\nExtracted pages: {len(pages)}")
    print(f"Created chunks: {len(chunks)}")

    print("\n--- Chunks containing 'file' or 'handling' ---")

    matches = [
        chunk for chunk in chunks
        if "file" in chunk["text"].lower()
        or "handling" in chunk["text"].lower()
    ]

    for chunk in matches:
        print(
            f"\nChunk {chunk['chunk_id']} | "
            f"PDF page {chunk['page_number']}"
        )
        print(chunk["text"])
        print("-" * 70)


if __name__ == "__main__":
    main()