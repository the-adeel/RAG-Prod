from tortoise import fields
from tortoise.models import Model

class DocumentChunk(Model):
    id = fields.IntField(pk=True)
    document_name = fields.CharField(max_length=255)
    chunk_index = fields.IntField()
    content = fields.TextField()
    faiss_id = fields.IntField(null=True)       # Links to the vector in FAISS
    metadata = fields.JSONField(null=True)

    class Meta:
        table = "document_chunk"