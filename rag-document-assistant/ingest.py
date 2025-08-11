import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Set your Google API key
# Make sure to set this environment variable in your system
os.environ["GOOGLE_API_KEY"] = "AIzaSyAWadfQpi95cG4HMDa1qZsVGlq9qdiXUaU"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 1. Load Documents
loader = PyPDFLoader("./documents/sample_test.pdf")
documents = loader.load()

# 2. Split Text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 3. Generate Embeddings with Google
# Using the same embedding model from your notebook
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 4. Create and Save Vector Store
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index") # Save the index to a local file

print("FAISS index has been created with Gemini embeddings and saved.")