# 📄 DocQuery: Chat with Your PDF Documents

DocQuery is a powerful and intuitive application that allows you to have conversations with your PDF documents. Simply upload a PDF, and the application will process it, enabling you to ask questions and receive intelligent, context-aware answers based on the document's content.

This project utilizes cutting-edge language models from Google, including `gemini-2.5-pro` and `embedding-001`, to provide a seamless and efficient question-answering experience. It offers two primary interfaces:
1.  **A user-friendly web application** built with Streamlit.
2.  **A simple REST API** created with Flask for programmatic access.

---

## ✨ Features

* **Interactive Chat Interface**: Upload a PDF and start asking questions right away through the Streamlit web app.
* **PDF Document Processing**: The application can ingest and process text from any PDF document using `PyPDFLoader`.
* **Advanced AI Integration**: Powered by Google's Gemini models for state-of-the-art text embedding and generation.
* **Efficient Vector Search**: Uses FAISS for rapid and accurate retrieval of relevant information from your documents.
* **Dual-Interface Access**: Interact via a web GUI (Streamlit) or a programmatic API (Flask).
* **Source Verification**: The web app displays the source text from the document that was used to generate the answer, allowing for easy verification.
* **Containerized Deployment**: Includes a `Dockerfile` for easy setup and deployment.

---

## ⚙️ How It Works

The project follows a Retrieval-Augmented Generation (RAG) architecture:

1.  **Document Ingestion & Chunking**: When a PDF is uploaded, its text content is extracted using `PyPDFLoader` and split into smaller, manageable chunks with `RecursiveCharacterTextSplitter`.
2.  **Embedding Generation**: Each text chunk is converted into a numerical representation (an embedding) using Google's `models/embedding-001`.
3.  **Vector Storage**: These embeddings are stored in a `FAISS` vector store, which is a highly efficient library for similarity searching.
4.  **Querying & Retrieval**: When you ask a question, it is also converted into an embedding. The system then searches the vector store to find the most relevant text chunks from the original document.
5.  **Answer Generation**: The retrieved chunks and your original question are passed to the `gemini-2.5-pro` model, which generates a coherent and contextually accurate answer.

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.11 or higher.
* An active **Google API Key**.

### Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install Dependencies**:
    Install all the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Your API Key**:
    You need to replace the placeholder `"YOUR GOOGLE_API_KEY"` with your actual Google API key in the following files:
    * `ingest.py`
    * `app.py`
    * `webapp.py`

### Running the Application

You can interact with this project through either the Streamlit web application or the Flask API.

#### 1. Running the Streamlit Web App

This is the recommended way to interact with the application visually.

 streamlit run webapp.py

## 2. Running the Flask API

The Flask application provides a REST endpoint for programmatic access.

### Step 1: Create the Vector Store

Before running the API, you must first process a document and create the FAISS index. Place your PDF file in a `documents` folder and run the `ingest.py` script.

python ingest.py
