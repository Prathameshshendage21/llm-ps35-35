import os

from dotenv import load_dotenv
from groq import Groq

from pdf_processor import retrieve_relevant_chunks


# Load environment variables
load_dotenv()

# Initialize Groq
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env file")

client = Groq(api_key=api_key)


def compare_documents(retrievers, question):
    """
    Compare multiple PDFs using Groq AI.

    Uses separate FAISS retrievers for each PDF
    and generates a structured comparison.
    """

    document_context = ""

    # Retrieve information separately from each PDF
    for document_name, retriever in retrievers.items():

        relevant_chunks = retrieve_relevant_chunks(
            retriever,
            question,
            top_k=4
        )

        document_context += f"\n\nDOCUMENT: {document_name}\n"

        for chunk_number, chunk in enumerate(
            relevant_chunks, start=1
        ):
            document_context += (
                f"\nRelevant Section {chunk_number}:\n"
                f"{chunk}\n"
            )

    # Build comparison prompt
    prompt = f"""
You are an intelligent PDF comparison assistant.

Your task is to compare information from multiple documents.

USER QUESTION:
{question}

DOCUMENT INFORMATION:
{document_context}

INSTRUCTIONS:

1. Answer using only the supplied document information.
2. Compare all documents wherever relevant.
3. Identify similarities and differences.
4. Present the comparison in a clear Markdown table.
5. Explain important findings after the table.
6. Mention document names when presenting information.
7. If information is missing, explicitly mention it.
8. Never invent facts or figures.

Provide a detailed and structured comparison.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError("Groq returned an empty response.")

        return result

    except Exception as error:
        raise RuntimeError(
            f"Groq API failed: {str(error)}"
        ) from error