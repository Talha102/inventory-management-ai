from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

def load_pdf(pdf_path):
    # Step 1: Read the PDF file
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Step 2: Split into small chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # Step 3: Convert chunks to numbers (embeddings)
    # Using free HuggingFace model — no API key needed
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Step 4: Store in FAISS vector database
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def get_answer(vectorstore, question):
    # Connect to Groq LLM (free & fast)
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Build RAG chain
    # retriever finds top 3 relevant chunks
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}
        ),
        return_source_documents=True
    )

    # Get answer from LLM
    result = qa_chain.invoke({"query": question})

    return {
        "answer": result["result"],
        "sources": result["source_documents"]
    }
