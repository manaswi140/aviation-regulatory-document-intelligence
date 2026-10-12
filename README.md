# Aviation Regulatory Document Intelligence System

A Python-based document intelligence application for searching aviation regulatory PDFs and retrieving relevant passages with source-page references. The project combines document processing, semantic search, and keyword relevance scoring in a Streamlit interface.

> **Important:** This is an educational software prototype for document discovery and review. It does not determine regulatory compliance, airworthiness, or certification status. Always verify findings against the applicable official, current regulatory material and approved procedures.

## Overview

Regulatory documents can be lengthy and difficult to navigate. This application helps users locate potentially relevant passages by asking a question about the documents they upload.

The application extracts text from PDFs, divides the extracted content into smaller chunks, indexes the content for retrieval, and presents relevant passages with source references. It is designed to support document review—not replace engineering judgement or an authoritative regulatory interpretation.

## Features

- **PDF upload and text extraction** using PyMuPDF.
- **Text chunking** to make long documents easier to search.
- **Semantic retrieval** using Sentence Transformers and FAISS.
- **Keyword relevance** using TF-IDF and scikit-learn.
- **Question-oriented search** across the processed document content.
- **Source traceability** through document/page references where available.
- **Streamlit interface** for interacting with the workflow.
- **Local persistence** for application data, according to the current implementation.
- **Automated tests** for key document-processing, search, workflow, and storage components.

### How answers are produced

The current implementation retrieves relevant passages and selects concise information from the retrieved text. **It does not currently generate answers using an LLM.** Treat the displayed content as search assistance and check the cited source passage directly.

## Architecture

```text
PDF upload
    |
    v
Text extraction (PyMuPDF)
    |
    v
Text cleaning and chunking
    |
    +----------------------------+
    |                            |
    v                            v
Semantic embeddings          TF-IDF keyword features
    |                            |
    v                            v
FAISS similarity search      Keyword relevance
    |                            |
    +-------------+--------------+
                  |
                  v
       Relevant passage retrieval
                  |
                  v
   Concise retrieved-text response
       + document/page references
```

## Technology stack

- **Language:** Python
- **User interface:** Streamlit
- **PDF processing:** PyMuPDF
- **Semantic search:** Sentence Transformers, FAISS
- **Keyword retrieval / data processing:** scikit-learn, Pandas
- **Testing:** Python test suite included in the repository

## Repository structure

The exact file layout may evolve as the project develops. The main components cover:

- PDF text extraction and document processing
- Chunking and search/index creation
- Semantic and keyword retrieval
- Streamlit application workflow
- Local data persistence
- Automated tests

Refer to the repository files for the current module names and implementation details.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/manaswi140/aviation-regulatory-document-intelligence.git
cd aviation-regulatory-document-intelligence
```

### 2. Create a virtual environment

**Windows (Command Prompt):**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository contains `requirements.txt`, install its pinned/project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is not present in the checked-out version, install the dependencies documented by the project and add a maintained `requirements.txt` before sharing the repository with others.

### 4. Run the application

For a Streamlit entry-point file named `app.py`, run:

```bash
streamlit run app.py
```

If the current entry-point filename differs, use that filename instead. Streamlit will print a local URL in the terminal; open it in your browser.

## Using the application

1. Start the Streamlit application.
2. Upload a text-based aviation regulatory PDF that you are permitted to use.
3. Allow the application to extract and process the document.
4. Enter a question about information that may be present in the uploaded material.
5. Review the retrieved passage and its document/page reference.
6. Open the source PDF and verify the context before relying on the result.

Search quality depends on the quality of the source PDF, the extracted text, the query, and the retrieval settings.

## Testing

Run the repository's tests from the project root using the test command supported by the current test layout. If the tests use `pytest`, run:

```bash
pytest -q
```

Record the actual test result when updating this section. Do not report a test count, coverage percentage, or accuracy score unless it has been measured against the current code.

## Evaluation roadmap

A useful next step is to build a small, manually reviewed evaluation set containing:

- A question about a known passage
- The expected relevant document and page
- The expected answer or supporting excerpt
- Questions that use different wording for the same concept
- Questions whose answers are absent from the documents

Use the set to compare retrieval configurations and report measured results, such as Precision@K, Recall@K, and source-page correctness where applicable. Keep the evaluation examples and scoring method documented so that results can be reproduced.

## Limitations

- **Scanned PDFs:** PDFs containing only page images may not yield searchable text without OCR.
- **Retrieval is not verification:** A relevant-looking passage may be incomplete or out of context.
- **No LLM-generated answer in the current implementation:** The application selects information from retrieved passages.
- **Document freshness:** Users must ensure they are working with the applicable and current revision of a regulatory document.
- **Local persistence:** The current prototype's storage behaviour may not be suitable for multi-user or production deployments.
- **Not a compliance decision system:** Search results must not be treated as an official determination of compliance, certification, or airworthiness.

## Responsible use and data handling

- Use documents you are authorized to process and share.
- Do not upload confidential, export-controlled, personal, or otherwise restricted material to an unapproved environment.
- Do not commit credentials, tokens, or sensitive documents to Git.
- Verify every important finding against the original source and the applicable approved process.

## Future improvements

- Add a labelled evaluation dataset and retrieval-quality measurements.
- Improve handling of empty, malformed, encrypted, and image-only PDFs.
- Add OCR support for scanned documents, if required.
- Improve user-facing error messages and test coverage.
- Optionally add **grounded LLM answers** that use retrieved passages only, show source citations, and abstain when evidence is insufficient. This should be described as an implemented feature only after it has been built and tested.
- Add an architecture image and screenshots from the running application.
- Deploy a demo only after confirming that the app works in the deployment environment.

## Disclaimer

This project is an educational prototype intended to assist with document search and review. It is not an official aviation authority tool and does not replace current regulations, approved technical data, professional engineering review, or formal airworthiness and certification processes.
