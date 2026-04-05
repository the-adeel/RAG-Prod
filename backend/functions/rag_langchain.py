from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os
import shutil
from .rerank import rerank
from models.doc import DocumentChunk


embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
vectorstore = None
VECTORSTORE_PATH = "vectorstore"


def load_vectorstore():
    """Load FAISS index from disk if it exists. Called at startup."""
    global vectorstore
    if (
        os.path.exists(VECTORSTORE_PATH)
        and os.path.isdir(VECTORSTORE_PATH)
        and os.path.exists(os.path.join(VECTORSTORE_PATH, "index.faiss"))
    ):
        vectorstore = FAISS.load_local(
            VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True
        )
        print(f"✅ FAISS vector store loaded from '{VECTORSTORE_PATH}'")
    else:
        print("ℹ️  No existing FAISS index found. Will create on first upload.")


async def add_file_to_vectorstore(file_path):
    """
    Process a file: split into chunks, store embeddings in FAISS,
    store metadata in PostgreSQL with faiss_id cross-references.
    Re-uploading the same file rebuilds the entire FAISS index.
    """
    global vectorstore

    filename = os.path.basename(file_path)

    # ── Check if this document already exists ──
    existing = await DocumentChunk.filter(document_name=filename).count()
    if existing > 0:
        # Delete old data for this file from Postgres
        await DocumentChunk.filter(document_name=filename).delete()
        # Rebuild entire FAISS index from remaining Postgres chunks
        await _rebuild_faiss_from_db()

    # ── Load document ──
    ext = file_path.lower().split(".")[-1]
    if ext == "txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == "pdf":
        loader = UnstructuredPDFLoader(file_path)
    elif ext in ["docx", "doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()

    # ── Split into chunks ──
    all_chunks = []
    for doc in documents:
        all_chunks.extend(splitter.split_text(doc.page_content))

    if not all_chunks:
        return f"File '{filename}' had no extractable text."

    # ── Add to FAISS ──
    if vectorstore is None:
        vectorstore = FAISS.from_texts(all_chunks, embeddings)
    else:
        vectorstore.add_texts(all_chunks)

    # The FAISS docstore assigns string IDs internally; we'll use the
    # index order. After adding, the latest IDs are at the end.
    # We need to get the FAISS internal IDs for the chunks we just added.
    # FAISS index total count after adding:
    total_vectors = vectorstore.index.ntotal
    start_faiss_id = total_vectors - len(all_chunks)

    # ── Save metadata to PostgreSQL with faiss_id ──
    db_chunks = []
    for i, text in enumerate(all_chunks):
        faiss_id = start_faiss_id + i
        db_chunks.append(
            DocumentChunk(
                document_name=filename,
                chunk_index=i,
                content=text,
                faiss_id=faiss_id,
                metadata={"source": filename, "chunk": i},
            )
        )

    await DocumentChunk.bulk_create(db_chunks)

    # ── Persist FAISS to disk ──
    vectorstore.save_local(VECTORSTORE_PATH)

    return f"File '{filename}' added successfully. {len(db_chunks)} chunks indexed."


async def _rebuild_faiss_from_db():
    """Rebuild the entire FAISS index from all remaining chunks in PostgreSQL."""
    global vectorstore

    remaining_chunks = await DocumentChunk.all().order_by("id")

    if not remaining_chunks:
        # No chunks left — clear FAISS
        vectorstore = None
        if os.path.exists(VECTORSTORE_PATH):
            shutil.rmtree(VECTORSTORE_PATH)
        print("🗑️  All chunks deleted. FAISS index cleared.")
        return

    texts = [chunk.content for chunk in remaining_chunks]
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Update faiss_ids in Postgres to match new index
    for i, chunk in enumerate(remaining_chunks):
        chunk.faiss_id = i
    await DocumentChunk.bulk_update(remaining_chunks, fields=["faiss_id"])

    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"🔄 FAISS index rebuilt with {len(texts)} chunks.")


async def retrieve(query: str, k: int = 5):
    """
    Retrieve relevant chunks using:
    1. FAISS semantic similarity search
    2. Cohere reranking
    3. PostgreSQL metadata lookup for source references
    """
    if not query or vectorstore is None:
        return []

    # ── Step 1: FAISS similarity search — get more candidates than needed ──
    faiss_results = vectorstore.similarity_search_with_score(query, k=k * 3)

    if not faiss_results:
        return []

    # Extract texts from FAISS results
    candidate_texts = [doc.page_content for doc, score in faiss_results]

    # ── Step 2: Rerank with Cohere ──
    reranked_texts = rerank(query, candidate_texts, top_k=k)

    # ── Step 3: Look up metadata from PostgreSQL ──
    result = []
    for text in reranked_texts:
        # Find the matching chunk in Postgres for source reference
        chunk = await DocumentChunk.filter(content=text).first()
        if chunk:
            result.append(
                {
                    "content": chunk.content,
                    "document": chunk.document_name,
                    "chunk_index": chunk.chunk_index,
                }
            )
        else:
            # Fallback if not found in DB (shouldn't happen normally)
            result.append(
                {
                    "content": text,
                    "document": "Unknown",
                    "chunk_index": -1,
                }
            )

    return result