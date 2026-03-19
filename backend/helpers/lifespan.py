from contextlib import asynccontextmanager
from tortoise import Tortoise, connections
from config import TORTOISE_ORM

@asynccontextmanager
async def lifespan(app):

    await Tortoise.init(config=TORTOISE_ORM)

    conn = connections.get("default")

    await conn.execute_query("CREATE EXTENSION IF NOT EXISTS vector")

    await conn.execute_query("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'document_chunk' AND column_name = 'embedding'
            ) THEN
                ALTER TABLE document_chunk ADD COLUMN embedding vector(384);
            END IF;
        END $$;
    """)

    yield

    await Tortoise.close_connections()