
import re

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(text):
    """Normalize text for reliable matching."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def is_table_of_contents(text):
    """Detect chunks that are likely to contain table-of-contents text."""
    markers = text.count("»") + text.count("›") + text.count("→")

    if markers >= 2:
        return True

    normalized = normalize_text(text)

    toc_phrases = [
        "introduction to files",
        "types of files",
        "opening and closing a text file",
        "writing to a text file",
        "reading from a text file",
        "setting offsets in a file",
    ]

    matched = sum(phrase in normalized for phrase in toc_phrases)

    return matched >= 3


class SemanticSearch:
    """Hybrid semantic and keyword search for document chunks."""

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.keyword_vectorizer = None
        self.keyword_matrix = None

    def build_index(self, chunks):
        """Build semantic and keyword indexes."""
        if not chunks:
            raise ValueError("Cannot build an index with no chunks.")

        texts = [chunk["text"].strip() for chunk in chunks]

        if any(not text for text in texts):
            raise ValueError("Chunks must not contain empty text.")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        embeddings = np.asarray(embeddings, dtype="float32")

        new_index = faiss.IndexFlatIP(embeddings.shape[1])
        new_index.add(embeddings)

        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english",
            token_pattern=r"(?u)\b\w+\b",
        )

        try:
            keyword_matrix = vectorizer.fit_transform(texts)
        except ValueError as error:
            if "empty vocabulary" not in str(error).lower():
                raise

            vectorizer = TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                sublinear_tf=True,
                token_pattern=r"(?u)\b\w+\b",
            )
            keyword_matrix = vectorizer.fit_transform(texts)

        # Update the active index only after building succeeds.
        self.index = new_index
        self.keyword_vectorizer = vectorizer
        self.keyword_matrix = keyword_matrix
        self.chunks = chunks

    def _question_boost(self, question, text):
        """Reward passages containing evidence relevant to the question."""
        q = normalize_text(question)
        t = normalize_text(text)
        boost = 0.0

        # Questions about file operations.
        if (
            "operation" in q
            and "file" in q
            and (
                "operations on files include" in t
                or (
                    "creating" in t
                    and "traversing" in t
                    and "reading" in t
                )
            )
        ):
            boost += 0.35

        # Questions about opening a file.
        if (
            "open" in q
            and "file" in q
            and (
                "open() function" in t
                or "file_object= open" in t
                or "file_object = open" in t
                or "syntax of open()" in t
            )
        ):
            boost += 0.35

        # Definition-style questions.
        if (
            q.startswith("what is ")
            or q.startswith("what are ")
            or q.startswith("define ")
            or q.startswith("definition of ")
        ):
            definition_cues = [
                " is defined as ",
                " is a ",
                " are ",
                " refers to ",
                " means ",
                " consists of ",
                " is the process of ",
            ]

            if any(cue in f" {t} " for cue in definition_cues):
                boost += 0.08

        # Penalize table-of-contents fragments.
        if is_table_of_contents(text):
            boost -= 0.30

        # A chapter heading alone is weaker evidence than an explanation.
        if (
            len(t) < 180
            and (
                "introduction to files" in t
                or "file handling in python" in t
            )
        ):
            boost -= 0.08

        return boost

    def search(self, question, top_k=3):
        """Retrieve the most relevant passages for a question."""
        if self.index is None:
            raise RuntimeError(
                "Search index is not ready. Build the index first."
            )

        if not question or not question.strip():
            raise ValueError("Question must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        question = question.strip()

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        semantic_scores, _ = self.index.search(
            query_embedding,
            len(self.chunks),
        )

        semantic_scores = semantic_scores[0]

        query_keywords = self.keyword_vectorizer.transform(
            [question]
        )

        keyword_scores = cosine_similarity(
            query_keywords,
            self.keyword_matrix,
        )[0]

        # Hybrid relevance score.
        combined_scores = (
            0.60 * semantic_scores
            + 0.40 * keyword_scores
        )

        # Apply question-specific evidence and quality adjustments.
        for i, chunk in enumerate(self.chunks):
            combined_scores[i] += self._question_boost(
                question,
                chunk["text"],
            )

        ranked_indices = np.argsort(combined_scores)[::-1][:top_k]

        results = []

        for position in ranked_indices:
            result = self.chunks[int(position)].copy()

            result["similarity_score"] = float(
                combined_scores[position]
            )
            result["semantic_score"] = float(
                semantic_scores[position]
            )
            result["keyword_score"] = float(
                keyword_scores[position]
            )

            results.append(result)

        return results