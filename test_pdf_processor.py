
from pathlib import Path
import pymupdf

from pdf_processor import extract_text_from_pdf


def test_extract_text_and_page_numbers():
    test_pdf = Path("test_document.pdf")

    with pymupdf.open() as document:
        first_page = document.new_page()
        first_page.insert_text((72, 72), "Aviation regulation test page one.")

        second_page = document.new_page()
        second_page.insert_text((72, 72), "Aviation regulation test page two.")

        document.save(test_pdf)

    try:
        pages = extract_text_from_pdf(test_pdf)

        assert len(pages) == 2
        assert pages[0]["page_number"] == 1
        assert pages[1]["page_number"] == 2
        assert "test page one" in pages[0]["text"]
        assert "test page two" in pages[1]["text"]

        print("PASS: PDF text extraction and page numbers work.")

    finally:
        test_pdf.unlink(missing_ok=True)


if __name__ == "__main__":
    test_extract_text_and_page_numbers()