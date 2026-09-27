from uuid import UUID
from sqlalchemy import text
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


from chat_svc.model.doc_model import Document,DocumentChunk

class ChunkRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_document(self, document_key: str):

        result = await self.session.execute(
            select(Document).where(
                Document.document_key == document_key
            )
        )

        return result.scalar_one_or_none()

    async def delete_chunks(self, document_id: UUID):

        await self.session.execute(
            delete(DocumentChunk).where(
                DocumentChunk.document_id == document_id
            )
        )

    async def add_chunk(self, chunk: DocumentChunk):
        self.session.add(chunk)

    async def add_document(self, document: Document):
         self.session.add(document)

    async def get_chunks_for_search(self, query_embedding: list[float], limit: int = 5):
        query = text("""
                SELECT
                    id,
                    content,
                    1 - (embedding <=> :query_embedding) AS similarity
                FROM document_chunks
                ORDER BY embedding <=> :query_embedding
                LIMIT :limit
            """)

        result = await self.session.execute(
                query,
                {
                    "query_embedding": query_embedding,
                    "limit": limit,
                },
            )

        return result.mappings().all()