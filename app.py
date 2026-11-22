import streamlit as st

from pdf_processor import (
    extract_text,
    split_text,
    create_retriever
)

from comparison import compare_documents


# Page configuration
st.set_page_config(
    page_title="Multi-PDF Comparison Tool",
    page_icon="📚",
    layout="wide"
)


# Application title
st.title("📚 Multi-PDF Comparison Tool")

st.markdown("""
### AI-powered document comparison

Upload 2–3 PDF documents, ask questions
and compare their contents using Generative AI.
""")

st.divider()


# Initialize session state
if "retrievers" not in st.session_state:
    st.session_state.retrievers = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# PDF upload section
st.header("1. Upload PDF Documents")

uploaded_files = st.file_uploader(
    "Choose 2 or 3 PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# Process documents
if st.button("Process Documents", type="primary"):

    if not uploaded_files or len(uploaded_files) < 2:
        st.error("Please upload at least 2 PDF documents.")

    elif len(uploaded_files) > 3:
        st.error("You can upload a maximum of 3 PDF documents.")

    else:

        retrievers = {}
        processed_files = []

        progress = st.progress(0)

        try:
            for i, pdf in enumerate(uploaded_files):

                st.write(f"Processing: {pdf.name}")

                # Extract PDF text
                text = extract_text(pdf)

                # Split text into chunks
                chunks = split_text(text)

                if not chunks:
                    raise ValueError(
                        f"No readable content in {pdf.name}"
                    )

                # Create separate FAISS retriever
                retriever = create_retriever(chunks)

                retrievers[pdf.name] = retriever

                processed_files.append(pdf.name)

                progress.progress(
                    (i + 1) / len(uploaded_files)
                )

            st.session_state.retrievers = retrievers

            st.session_state.processed_files = processed_files

            st.success("All PDF documents processed successfully!")

        except Exception as e:
            st.error(f"Processing failed: {str(e)}")


# Display processed documents
if st.session_state.processed_files:

    st.divider()

    st.header("2. Uploaded Documents")

    for filename in st.session_state.processed_files:
        st.success(f"📄 {filename}")


    # Question section
    st.divider()

    st.header("3. Ask a Comparison Question")

    question = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: Compare the objectives, "
            "methodologies and results of all documents."
        ),
        height=120
    )

    if st.button("Generate Comparison"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Gemini AI is comparing your documents..."
            ):

                try:

                    result = compare_documents(
                        st.session_state.retrievers,
                        question
                    )

                    st.session_state.last_result = result

                    st.session_state.last_question = question

                except Exception as e:
                    st.error(f"Comparison failed: {str(e)}")


    # Display comparison
    if "last_result" in st.session_state:

        st.divider()

        st.header("4. AI Comparison Results")

        st.markdown(st.session_state.last_result)

        st.download_button(
            label="Download Comparison",
            data=st.session_state.last_result,
            file_name="PDF_Comparison.md",
            mime="text/markdown"
        )


# Footer
st.divider()

st.caption(
    "Multi-PDF Comparison Tool | "
    "GenAI Mini Project | Problem Statement 35"
)