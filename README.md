# Aviation Regulatory Document Intelligence System

A Python-based document intelligence application that allows users to upload PDF documents, ask questions about their contents, and retrieve relevant information with source references.

## Features

* PDF text extraction with page numbers using PyMuPDF.
* Text chunking to prepare documents for retrieval.
* Semantic search using Sentence Transformers.
* Keyword relevance using TF-IDF.
* FAISS-based similarity search.
* Concise answers selected from retrieved document passages.
* Source document and page references.
* Local persistence of processed text chunks.
* Interactive web interface built with Streamlit.

## Technology Stack

* Python 3.11
* Streamlit
* PyMuPDF
* Sentence Transformers
* FAISS
* Scikit-learn
* Pandas

## Architecture

1. **Document ingestion:** Accept PDF uploads and extract text with page metadata.
2. **Text processing:** Clean and split extracted text into searchable chunks.
3. **Indexing:** Generate text embeddings and build a FAISS search index.
4. **Retrieval:** Combine semantic similarity and keyword relevance to rank passages.
5. **Answer selection:** Select a relevant sentence from the retrieved passages.
6. **Source attribution:** Display the source document and page number.
7. **Persistence:** Save processed chunks locally for use after restarting the application.

## Project Structure

```text
Aviation regulatory system/
├── app.py
├── pdf_processor.py
├── text_chunker.py
├── semantic_search.py
├── document_pipeline.py
├── answer_generator.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
```

The project also includes Python test files for the processing, search, answer selection, workflow, and storage components.

## Installation

### Prerequisites

* Python 3.11
* Conda
* Git

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Aviation regulatory system"
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Create and activate a Conda environment

```bash
conda create -n aviation_ai python=3.11 -y
conda activate aviation_ai
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal.

## How to Use

1. Upload one or more text-based PDF documents.
2. Wait for processing and indexing to finish.
3. Enter a question about the uploaded documents.
4. Review the answer and its source reference.
5. Expand the source passage to verify the information in the original document.

## Testing

Run the tests from the project directory:

```bash
python test_pdf_processor.py
python test_text_chunker.py
python test_semantic_search.py
python test_document_pipeline.py
python test_answer_generator.py
python test_answer_quality.py
python test_full_workflow.py
python test_storage.py
```

## Current Limitations

* Scanned PDFs may require OCR, which is not currently included.
* Answers are selected from retrieved text; this is not an LLM-generated answer system.
* Search quality depends on document formatting, extracted text, and question wording.
* Local storage is intended for a prototype and does not provide multi-user access control.
* Important technical and regulatory information must be verified against the original document.

## Future Enhancements

* OCR support for scanned documents.
* Improved retrieval ranking and evaluation.
* More robust duplicate-document detection.
* Support for additional document formats.
* Evaluation using a curated set of questions and expected answers.
* Optional LLM-based answering with source-grounding checks.

## Disclaimer

This project is an educational document intelligence prototype. Its output should not be treated as an authoritative regulatory or compliance decision without verification against the original source documents.
