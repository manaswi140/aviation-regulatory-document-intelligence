
import re


def clean_page_text(text):
    """Remove table-of-contents entries, running headers, and page noise."""

    # Remove the quotation and its attribution, even if PDF line breaks
    # split the quotation across multiple lines.
    text = re.sub(
        r"there are many ways of trying to understand programs"
        r".*?robin milner",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    lines = text.splitlines()
    cleaned_lines = []
    in_contents = False

    for line in lines:
        stripped = line.strip()
        normalized = re.sub(r"\s+", " ", stripped).lower()

        if not stripped:
            continue

        # Detect the start of the table of contents.
        if normalized == "in this chapter":
            in_contents = True
            continue

        # Skip table-of-contents entries until the actual introduction.
        if in_contents:
            if re.match(
                r"^2\.1\s+introduction\s+to\s+files\b",
                normalized,
            ):
                in_contents = False
                cleaned_lines.append(stripped)
            continue

        # Remove common running headers and page labels.
        if normalized in {
            "computer science - class xii",
            "file handling in python",
            "2 file handling in python",
            "rationalised 2023-24",
        }:
            continue

        # Remove the vertically split word "Chapter".
        if re.fullmatch(r"c\s*h\s*a\s*p\s*t\s*e\s*r", normalized):
            continue

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def split_into_sentences(text):
    """Split text approximately at sentence boundaries."""
    return re.split(r"(?<=[.!?])\s+", text.strip())


def chunk_pages(
    pages,
    document_name="document",
    chunk_size=1000,
    overlap=150,
):
    """Create overlapping chunks with source document and page metadata."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = clean_page_text(page["text"])

        if not text.strip():
            continue

        # Normalize PDF line wrapping while preserving paragraph spacing.
        paragraphs = [
            re.sub(r"\s+", " ", paragraph).strip()
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]

        page_text = " ".join(paragraphs)

        if not page_text:
            continue

        start = 0

        while start < len(page_text):
            end = min(start + chunk_size, len(page_text))

            if end < len(page_text):
                # Prefer a sentence boundary.
                sentence_boundary = page_text.rfind(". ", start, end)

                if sentence_boundary > start + chunk_size // 2:
                    end = sentence_boundary + 1
                else:
                    # Otherwise, avoid splitting a word.
                    space_boundary = page_text.rfind(" ", start, end)

                    if space_boundary > start:
                        end = space_boundary

            chunk_text = page_text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": len(chunks),
                        "document_name": document_name,
                        "page_number": page_number,
                        "text": chunk_text,
                    }
                )

            if end >= len(page_text):
                break

            start = max(start + 1, end - overlap)

            # Move forward to a word boundary.
            next_space = page_text.find(" ", start)

            if next_space != -1 and next_space < end:
                start = next_space + 1

    return chunks
