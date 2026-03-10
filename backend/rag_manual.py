import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from documents import documents

model = SentenceTransformer('BAAI/bge-base-en')

def get_embedding(text):
    return model.encode(text)

doc_embeddings = [get_embedding(doc) for doc in documents]

dimension = len(doc_embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(np.array(doc_embeddings).astype("float32"))


def retrieve(query, k=2):

    query_embedding = get_embedding(query)

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = [documents[i] for i in indices[0]]

    return results