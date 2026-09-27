from fastapi import FastAPI, Depends
import uvicorn
from chat_svc.config.envconfig import settings
from chat_svc.model.msg_model import ChatModel
from chat_svc.service.chat_service import ChatService
from chat_svc.repos.connectivity import Connect
from google import genai
from chat_svc.config.envconfig import settings
app = FastAPI()
from chat_svc.embeddings.store_chunks import StoreChunk
from chat_svc.db.connect import AsyncSessionLocal
from chat_svc.db.connect import get_session
from chat_svc.repos.chunk_repos import ChunkRepository
#move this to seperate file
client = genai.Client(
    api_key=settings.API_KEY
)


@app.on_event("startup")
async def ingest_document():
    async with AsyncSessionLocal() as session:
        store_chunks = StoreChunk(session)
        result = await store_chunks.ingest_doc(
            path=settings.INGEST_DOC_PATH,
            document_key=settings.INGEST_DOC_KEY,
        )
        print(result)


@app.post("/v1/chat")
async def chat(request:ChatModel):
    connct = Connect(client)
    chat_service = ChatService(connct)
    text = await chat_service.SendMessage(request)
    return{
        "response": text
    }


@app.post("/v2/chat")
async def chat(request:ChatModel,db: AsyncSessionLocal = Depends(get_session)):
    chunk_repos = ChunkRepository(db)
    connct = Connect(client, chunk_repos)
    chat_service_v2 = ChatService(connct)
    text = await chat_service_v2.search(request)
    return{
        "response": text
    }

if __name__ == "__main__":
    uvicorn.run("chat_svc.main:app",host="127.0.0.1",port = settings.port, reload = True)