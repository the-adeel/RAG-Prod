import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from document import document

model = SentenceTransformer('BAAI/bge-base-en')

def chunk_text(text, chunk_size=5, overlap=2):
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

def get_embedding(text):
    return model.encode(text)

all_chunks = chunk_documents(document)
doc_embeddings = [get_embedding(chunk) for chunk in all_chunks]
dimension = len(doc_embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings).astype("float32"))

def retrieve(query, k=2):
    query_embedding = get_embedding(query)
    query_vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vector, k)
    results = [all_chunks[i] for i in indices[0]]

    return results