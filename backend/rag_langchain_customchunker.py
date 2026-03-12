from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def load_documents(folder="uploads"):
    docs = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        with open(path, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def add_file_to_vectorstore(file_path):
    global vectorstore

    # Determine loader based on file extension
    ext = file_path.lower().split('.')[-1]
    if ext == "txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == "pdf":
        loader = UnstructuredPDFLoader(file_path)
    elif ext in ["docx", "doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Load and split documents
    documents = loader.load()
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc.page_content))

    # Create a new vector store every time
    vectorstore = FAISS.from_texts(all_chunks, embeddings)
    vectorstore.save_local("vectorstore")

    return f"File '{file_path}' added to vector store successfully."

# retrieval
def retrieve(query, k=2):
    docs = vectorstore.similarity_search(query, k=k)
    results = [doc.page_content for doc in docs]
    return results