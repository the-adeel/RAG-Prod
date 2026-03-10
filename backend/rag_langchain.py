from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from documents import documents

# embeddings wrapper
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")

# create vector store (FAISS index internally)
vectorstore = FAISS.from_texts(documents, embeddings)

# retrieval
def retrieve(query, k=2):
    docs = vectorstore.similarity_search(query, k=k)
    results = [doc.page_content for doc in docs]
    return results