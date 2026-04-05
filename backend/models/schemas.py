from pydantic import BaseModel
from typing import Optional, Dict, Any

class DocumentChunkSchema(BaseModel):
    id: int
    document_name: str
    chunk_index: int
    content: str
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True