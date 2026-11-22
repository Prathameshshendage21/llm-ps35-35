# Multi-PDF Comparison Tool

**GenAI Mini Project – Problem Statement 35**

## 1. Project Overview

The Multi-PDF Comparison Tool is an AI-powered application that allows users to upload and compare multiple PDF documents. Instead of manually reading several documents, users can ask questions and receive structured comparisons generated using a Large Language Model (LLM).

The application retrieves relevant information from each PDF separately and generates a comparison table with important findings.

## 2. Features

- Upload and compare 2–3 PDF documents.
- Extract text from PDF files.
- Split extracted text into smaller chunks.
- Generate text embeddings using Sentence Transformers.
- Create separate FAISS vector indexes for each PDF.
- Retrieve relevant information based on user questions.
- Generate AI-powered comparisons using Groq.
- Display results in structured Markdown tables.
- Download comparison results.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Groq API | AI-powered comparison |
| Google Gemini | Initially tested as an LLM provider |

## 4. Project Structure

```text
PDFTool/
│
├── app.py
├── pdf_processor.py
├── comparison.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── sample_pdfs/
├── screenshots/
│
└── .env (not uploaded)
```

## 5. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-ps35-35.git
```

### Step 2: Open the Project Folder

```bash
cd llm-ps35-35
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure the API Key

Create a `.env` file in the project directory and add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key.

**Important:** Never upload your API key or `.env` file to GitHub.

### Step 6: Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 6. Working Procedure

1. The user uploads two or three PDF documents.
2. The application extracts text from each PDF using PyPDF.
3. Extracted text is divided into smaller chunks.
4. Sentence Transformers generates embeddings for the chunks.
5. FAISS creates a separate vector index for each document.
6. The user enters a comparison question.
7. The system retrieves relevant chunks separately from each document.
8. Retrieved information is combined into a comparison prompt.
9. Groq generates a structured response using the retrieved information.
10. The application displays the comparison and allows the user to download the result.

## 7. Example Input

**Uploaded Documents:**
- Attention Is All You Need
- BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

**Example Question:**

Compare the main objectives, methodology, and key findings of these two research papers.

## 8. Output

The application generates:
- A comparison table.
- Similarities and differences.
- Important findings.
- A summary of the documents.

## 9. Limitations

- Scanned PDFs without extractable text are not supported by the current text-extraction implementation.
- The quality of the comparison depends on the information retrieved from the uploaded documents.
- Internet connectivity and a valid Groq API key are required for AI-generated comparisons.
- API usage may be subject to provider rate limits.

## 10. Conclusion

The Multi-PDF Comparison Tool simplifies document analysis by combining PDF text extraction, semantic search, vector databases, and Generative AI. It helps users compare multiple documents efficiently and obtain structured answers without manually reviewing every page.