class Connect:
    def __init__(self,client, chunk_repos):
        self.client = client
        self.chunk_repos = chunk_repos

    async def getResponse(self, msg):
        response =  self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=msg
        )
        print(response.text)
        return response.text

    async def search(self, msg):
        embedding = (await self.create_embedding(msg))
        chunks = await self.chunk_repos.get_chunks_for_search(embedding,limit=5)
        return await self.get_answer_from_chunks(chunks, msg)

    async def create_embedding(self, text: str) -> str:
        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
             config={
                "output_dimensionality": 768
            },
        )
        return str(response.embeddings[0].values)

    async def get_answer_from_chunks(self, chunks, query):
        context = "\n".join([chunk["content"] for chunk in chunks])
        prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text