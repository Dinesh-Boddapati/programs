import os
import streamlit as st
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
import tempfile

import nest_asyncio
nest_asyncio.apply()


os.environ["GOOGLE_API_KEY"] = "YOUR GOOGLE_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- Helper Functions ---
def get_pdf_text_and_metadata(pdf_file):
    """Extracts text and metadata from an uploaded PDF file."""
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()
    os.remove(tmp_file_path) # Clean up the temporary file
    return documents

def create_vector_store(documents):
    """Creates a FAISS vector store from the given documents."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(docs, embeddings)
    return db

def create_qa_chain(db):
    """Creates a RetrievalQA chain from the vector store."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.1)
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# --- Streamlit App ---
st.set_page_config(page_title="DocQuery", page_icon="📄")
st.title("📄 DocQuery: Chat with Your Documents")

# File uploader in the sidebar
with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Main app logic
if uploaded_file is not None:
    # Check if a new file has been uploaded
    # We use the file's name and size as a simple check
    if "qa_chain" not in st.session_state or \
       st.session_state.file_name != uploaded_file.name or \
       st.session_state.file_size != uploaded_file.size:

        st.session_state.file_name = uploaded_file.name
        st.session_state.file_size = uploaded_file.size

        # Process the new file
        with st.spinner("Processing document... Please wait."):
            try:
                documents = get_pdf_text_and_metadata(uploaded_file)
                db = create_vector_store(documents)
                st.session_state.qa_chain = create_qa_chain(db)
                st.success("Document processed successfully! You can now ask questions.")
            except Exception as e:
                st.error(f"An error occurred during document processing: {e}")
                st.stop()

    # Chat interface
    st.header("Ask a Question")
    user_question = st.text_input("What would you like to know from the document?")

    if user_question:
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.qa_chain.invoke(user_question)
                st.write("### Answer")
                st.write(response["result"])

                with st.expander("Show Source Documents"):
                    st.write(response["source_documents"])
            except Exception as e:
                st.error(f"An error occurred while getting the answer: {e}")

else:
    st.info("Please upload a PDF document in the sidebar to get started.")