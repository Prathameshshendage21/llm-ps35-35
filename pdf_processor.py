import faiss
import numpy as np

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def extract_text(pdf_file):
    """
    Extract text from an uploaded PDF.
    """

    reader = PdfReader(pdf_file)

    text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            text += f"\n[Page {page_number}]\n{page_text}"

    if not text.strip():
        raise ValueError(
            "No readable text found. The PDF may be scanned."
        )

    return text


def split_text(text, chunk_size=500, overlap=100):
    """
    Split document text into smaller chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_retriever(chunks):
    """
    Create a separate FAISS index for a PDF.
    """

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return {
        "index": index,
        "chunks": chunks
    }


def retrieve_relevant_chunks(retriever, question, top_k=4):
    """
    Retrieve relevant chunks from a PDF.
    """

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    scores, indices = retriever["index"].search(
        question_embedding,
        min(top_k, len(retriever["chunks"]))
    )

    results = []

    for idx in indices[0]:

        if idx != -1:
            results.append(retriever["chunks"][idx])

    return results