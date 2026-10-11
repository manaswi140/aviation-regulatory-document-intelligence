import streamlit as st

from document_pipeline import DocumentPipeline
from answer_generator import generate_answer
from storage import save_chunks, load_chunks


st.set_page_config(
    page_title="Aviation Regulatory Document Intelligence",
    page_icon="📄",
    layout="wide",
)

st.title("Aviation Regulatory Document Intelligence System")
st.write(
    "Upload PDF documents and ask questions to find "
    "relevant information with source references."
)


# --------------------------------------------------
# 1. Initialize the application and restore saved data
# --------------------------------------------------

if "pipeline" not in st.session_state:
    st.session_state.pipeline = DocumentPipeline()

if "all_chunks" not in st.session_state:
    try:
        st.session_state.all_chunks = load_chunks()
    except RuntimeError as error:
        st.session_state.all_chunks = []
        st.error(str(error))

if "processed_names" not in st.session_state:
    st.session_state.processed_names = {
        chunk.get("document_name")
        for chunk in st.session_state.all_chunks
        if chunk.get("document_name")
    }

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

    if st.session_state.all_chunks:
        try:
            with st.spinner("Restoring the saved search index..."):
                st.session_state.pipeline.build_search_index(
                    st.session_state.all_chunks
                )

            st.session_state.index_ready = True

        except Exception as error:
            st.error(f"Could not restore the search index: {error}")


# --------------------------------------------------
# 2. Display saved document information
# --------------------------------------------------

st.header("1. Your documents")

if st.session_state.all_chunks:
    st.success(
        f"{len(st.session_state.all_chunks)} saved text chunks "
        "are available for searching."
    )

    document_names = sorted(st.session_state.processed_names)

    st.write("**Saved documents:**")
    for name in document_names:
        st.write(f"- {name}")
else:
    st.info("No saved documents yet. Upload a PDF to get started.")


# --------------------------------------------------
# 3. Upload and process new PDF documents
# --------------------------------------------------

st.subheader("Upload new PDFs")

uploaded_files = st.file_uploader(
    "Choose one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

if st.button("Process documents", type="primary"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    else:
        new_chunks = []
        errors = []

        with st.spinner("Extracting and processing PDF documents..."):
            for uploaded_file in uploaded_files:
                if uploaded_file.name in st.session_state.processed_names:
                    st.info(
                        f"Skipped {uploaded_file.name}: "
                        "a document with this filename is already loaded."
                    )
                    continue

                try:
                    chunks = st.session_state.pipeline.process_pdf(
                        uploaded_file
                    )

                    new_chunks.extend(chunks)

                except Exception as error:
                    errors.append(f"{uploaded_file.name}: {error}")

        if new_chunks:
            updated_chunks = (
                st.session_state.all_chunks + new_chunks
            )

            try:
                # Save first so existing session data is not replaced
                # if saving fails.
                save_chunks(updated_chunks)

                st.session_state.all_chunks = updated_chunks

                for chunk in new_chunks:
                    name = chunk.get("document_name")
                    if name:
                        st.session_state.processed_names.add(name)

                with st.spinner("Building the search index..."):
                    st.session_state.pipeline.build_search_index(
                        st.session_state.all_chunks
                    )

                st.session_state.index_ready = True

                st.success(
                    f"Successfully saved and indexed "
                    f"{len(new_chunks)} new text chunks."
                )

            except Exception as error:
                st.error(
                    f"Could not save or index the new documents: {error}"
                )

        for error in errors:
            st.error(error)

        if not new_chunks and not errors:
            st.info("No new documents were processed.")


# --------------------------------------------------
# 4. Ask questions about the documents
# --------------------------------------------------

st.divider()
st.header("2. Ask a question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: What does the document explain?",
)

top_k = st.slider(
    "Number of relevant passages",
    min_value=1,
    max_value=10,
    value=3,
)

if st.button("Get answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    elif not st.session_state.index_ready:
        st.warning("Please upload and process at least one PDF first.")

    else:
        try:
            with st.spinner("Searching documents and generating an answer..."):
                results = st.session_state.pipeline.search(
                    question,
                    top_k=top_k,
                )

                response = generate_answer(question, results)

            st.subheader("Answer")
            st.write(response["answer"])

            st.subheader("Sources")

            if response["sources"]:
                for source in response["sources"]:
                    st.markdown(
                        f"**Document:** {source['document_name']}  \n"
                        f"**Page:** {source['page_number']}"
                    )

                    with st.expander("View source passage"):
                        st.write(source["text"])
            else:
                st.info("No source passages were identified.")

            if results:
                st.divider()
                st.subheader("Retrieved passages")

                for number, result in enumerate(results, start=1):
                    with st.expander(
                        f"Result {number} — "
                        f"{result['document_name']} "
                        f"(Page {result['page_number']})",
                        expanded=(number == 1),
                    ):
                        st.write(result["text"])
                        st.caption(
                            "Similarity score: "
                            f"{result['similarity_score']:.3f}"
                        )
            else:
                st.info(
                    "No relevant passages were found in the documents."
                )

        except Exception as error:
            st.error(f"Could not generate the answer: {error}")


# --------------------------------------------------
# 5. Application information
# --------------------------------------------------

st.divider()

st.caption(
    "Document chunks are stored locally in the data folder. "
    "Answers are based on retrieved passages; check the original "
    "document before relying on important technical information."
)

