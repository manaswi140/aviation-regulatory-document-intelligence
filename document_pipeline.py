
from pdf_processor import extract_text_from_pdf
from text_chunker import chunk_pages
from semantic_search import SemanticSearch


class DocumentPipeline:
    """Process PDFs and search their extracted content."""

    def __init__(self):
        self.search_engine = SemanticSearch()
        self.processed_documents = []
        self.is_ready = False

    def process_pdf(self, uploaded_file):
        """Extract, chunk, and index one uploaded PDF."""

        pages = extract_text_from_pdf(uploaded_file)

        if not pages:
            raise ValueError(
                f"No extractable text found in {uploaded_file.name}."
            )

        
        chunks = chunk_pages(
                pages,
                document_name=uploaded_file.name,
                chunk_size=500,
                overlap=80,
        )

        if not chunks:
            raise ValueError(
                f"No searchable text chunks found in {uploaded_file.name}."
            )

        self.processed_documents.append({
            "document_name": uploaded_file.name,
            "page_count": len(pages),
            "chunk_count": len(chunks),
        })

        self.is_ready = False
        return chunks

    def build_search_index(self, all_chunks):
        """Build one index containing chunks from all PDFs."""

        self.search_engine.build_index(all_chunks)
        self.is_ready = True

    def search(self, question, top_k=3):
        """Search the processed documents."""

        if not self.is_ready:
            raise RuntimeError(
                "Process documents and build the search index first."
            )

        return self.search_engine.search(question, top_k=top_k)