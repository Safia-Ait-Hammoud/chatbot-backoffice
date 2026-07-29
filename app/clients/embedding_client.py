from openai import OpenAI, AsyncOpenAI
from app.core.config import Settings


class EmbeddingClient:
    def __init__(self, settings: Settings):
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._async_client = AsyncOpenAI(api_key=settings.openai_api_key)  # ← ajouté
        self._model = settings.openai_embedding_model

    def generate(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            model=self._model,
            input=text,
        )
        return response.data[0].embedding

    async def generate_many(self, texts: list[str]) -> list[list[float]]:
        """Génère les embeddings de plusieurs textes en un seul appel (batch)."""
        if not texts:
            return []

        response = await self._async_client.embeddings.create(
            model=self._model,
            input=texts,
        )
        return [item.embedding for item in response.data]