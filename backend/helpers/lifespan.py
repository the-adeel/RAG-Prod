from contextlib import asynccontextmanager
from tortoise import Tortoise, connections
from config import TORTOISE_ORM

@asynccontextmanager
async def lifespan(app):

    await Tortoise.init(config=TORTOISE_ORM)

    conn = connections.get("default")

    # ── Schema migration: ensure document_chunk table has the right shape ──
    # Drop old embedding column if it exists
    await conn.execute_query("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'document_chunk' AND column_name = 'embedding'
            ) THEN
                ALTER TABLE document_chunk DROP COLUMN embedding;
            END IF;
        END $$;
    """)

    # Add faiss_id column if it doesn't exist
    await conn.execute_query("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'document_chunk' AND column_name = 'faiss_id'
            ) THEN
                ALTER TABLE document_chunk ADD COLUMN faiss_id INTEGER;
            END IF;
        END $$;
    """)

    # ── Pre-load FAISS vector store if it exists on disk ──
    from functions.rag_langchain import load_vectorstore
    load_vectorstore()

    yield

    await Tortoise.close_connections()