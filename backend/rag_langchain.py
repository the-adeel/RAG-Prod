from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from document import document

# embeddings wrapper
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def chunk_documents(documents):
    doc_chunks = []
    for doc in documents:
        doc_chunks.extend(chunk_text(doc, chunk_size=5, overlap=2))
    return doc_chunks

all_chunks = chunk_documents(document)

# create vector store (FAISS index internally)
vectorstore = FAISS.from_texts(all_chunks, embeddings)

# retrieval
def retrieve(query, k=2):
    docs = vectorstore.similarity_search(query, k=k)
    results = [doc.page_content for doc in docs]
    return results