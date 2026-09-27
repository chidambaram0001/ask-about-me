from datetime import datetime
from uuid import UUID,uuid4
from pgvector.sqlalchemy import VECTOR
from sqlalchemy import(DateTime,ForeignKey,Index,Integer,String,Text,UniqueConstraint,func)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

embedding_diemension = 768

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"
    id:Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),primary_key=True, default=uuid4)
    document_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    file_name:Mapped[str] = mapped_column(String(500),nullable=False)
    content_hash:Mapped[str]= mapped_column(String(64),nullable=False)
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    doc_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False,default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    document_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    section: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(embedding_diemension),
        nullable=False,
    )

    doc_metadata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk_index",
        ),

        Index(
            "ix_document_chunks_document_id",
            "document_id",
        ),

        Index(
            "ix_document_chunks_section",
            "section",
        ),

        Index(
            "ix_document_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={
                "embedding": "vector_cosine_ops"
            },
        ),
    )