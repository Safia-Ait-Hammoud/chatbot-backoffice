
from core.settings import settings
from openai import AsyncOpenAI


class EmbeddingService: 
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
        # 1536 pour text-embedding-3-small, 3072 pour text-embedding-3-large
        self.dimensions = settings.DIMENSIONS


    async def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
    
        return [item.embedding for item in response.data]