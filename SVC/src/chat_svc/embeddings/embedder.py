import asyncio
from google import genai
from google.genai import types
from chat_svc.config.envconfig import settings

class GeminiEmbedder:
    def __init__(self):
        self.client = genai.Client(api_key = settings.API_KEY)
    
    async def embedd_Doc(self, title:str, content:str) -> list:
        text = (
            f"title: {title} | "
            f"text: {content}"
        )
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=settings.embedding_dimension,
            ),
        )

        return list(response.embeddings[0].values)
    
    async def create_embedding(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
        )

        return response.embeddings[0].values