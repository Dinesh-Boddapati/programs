import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "YOUR GOOGLE_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)

# Load the FAISS index created with Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

# Create the RetrievalQA chain with the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.1)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Question not provided"}), 400

    try:
        response = qa_chain.invoke(question)
        return jsonify({"answer": response.get('result')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)