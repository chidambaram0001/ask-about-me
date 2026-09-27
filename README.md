The ingestion process reads the profile/resume document, splits it into smaller chunks, generates vector embeddings for each chunk, and stores the chunks and embeddings in PostgreSQL with pgvector.

Ingestion Flow
Profile / Resume Document

          ↓
       Load File
       
          ↓
      Clean Text
      
          ↓
       Chunk Text
       
          ↓
   Generate Embeddings
   
          ↓
 Store in PostgreSQL + pgvector
 
Run Ingestion

From the backend directory:

cd chat-svc

Run the ingestion command:

uv run python -m chat_svc.main

The command will:

Read the source document from the configured assets directory.
Split the document into chunks.
Generate an embedding for each chunk.
Store the chunks and embeddings in PostgreSQL.
Make the data available for semantic retrieval during chat.
Example
$ uv run python -m chat_svc.main

Starting document ingestion...
Reading document: assets/***.txt
Creating document chunks...
Generating embeddings...
Storing chunks in PostgreSQL...
Ingestion completed successfully.

env:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ragdb

GEMINI_API_KEY=your_gemini_api_key


EMBEDDING_MODEL=your_embedding_model


EMBEDDING_DIMENSION=768




**Screenshot**
<img width="1355" height="687" alt="ref" src="https://github.com/user-attachments/assets/4e2dd61a-1bf4-410c-9a74-0284406450cc" />
