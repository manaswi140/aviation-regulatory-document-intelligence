
import pymupdf


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF and preserve its original page numbers.
    Accepts a Streamlit UploadedFile or a PDF file path.
    """
    pages = []

    if hasattr(pdf_file, "getvalue"):
        # Streamlit uploaded file
        pdf_bytes = pdf_file.getvalue()
        document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    else:
        # Local PDF file path
        document = pymupdf.open(pdf_file)

    with document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text,
                })

    return pages