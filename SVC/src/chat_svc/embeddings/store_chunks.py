from concurrent.futures import __dir__

from chat_svc.embeddings.chunker import ResumeChunker
from chat_svc.embeddings.embedder import GeminiEmbedder
from chat_svc.model.doc_model import Document, DocumentChunk
from chat_svc.repos.chunk_repos import ChunkRepository
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
#from chat_svc.db.connect import get_session
class StoreChunk:
    def __init__( self, session: AsyncSession):
        self.session = session
        self.chunker = ResumeChunker()
        self.embedder = GeminiEmbedder()
        self.repos = ChunkRepository(session)

    async def ingest_doc(self, path:str, document_key):
        PROJECT_ROOT = Path(__file__).resolve().parents[3]
        file_path = (PROJECT_ROOT/ "assets"/ "chidambaram_resume_rag.txt")
        text =  Path(file_path).read_text(encoding='utf-8')
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing = await self.repos.get_document(
            document_key
        )
        if existing :
            if existing.content_hash == content_hash:
                return {
                        "status": "SKIPPED",
                        "document_id": str(
                            existing.id
                        ),
                        "reason": "Document already ingested",
                    }
            existing.version += 1
            existing.content_hash = content_hash

            document = existing

            await self.repos.delete_chunks(
                document.id
            )
            document = Document(document_key=document_key, file_name = file_path.name, 
            content_hash = content_hash, version = 1, doc_metadata = {
                "type":"txt"
            })
            await self.repos.add_document(document)
            await self.session.commit()

        else :
            document = Document(document_key=document_key, file_name = file_path.name, 
            content_hash = content_hash, version = 1, doc_metadata = {
                "type":"txt"
            })
            await self.repos.add_document(document)
            await self.session.commit()
    

        chunks = self.chunker.chunk(text)

        for chunk in chunks:
            embeddings = await self.embedder.embedd_Doc((f"{document.file_name} - {chunk.section}"),chunk.content)
            print(type(embeddings))
            doc_chunk = DocumentChunk(
                 document_id=document.id,
                chunk_index=chunk.index,
                section=chunk.section,
                content=chunk.content,
                content_hash=chunk.metadata[
                    "content_hash"
                ],
                token_count=0,
                embedding=embeddings,
                doc_metadata={
                    **chunk.metadata,
                    "document_version": (
                        document.version
                    ),
                },
            )
            await self.repos.add_chunk(
                doc_chunk
            )

        await self.session.commit()
      

        return {
            "status": "INGESTED",
            "document_id": str(document.id),
            "version": document.version,
            "chunks": len(chunks),
        }

        
