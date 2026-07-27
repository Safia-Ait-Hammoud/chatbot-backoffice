from core.dependencies import get_embedding_service
from core.settings import settings
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from fastapi import HTTPException
from repositories.project_repository import ProjectRepository






class ChatService:
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.qdrant_client = settings.QDRANT_CLIENT
        self.project_repository = ProjectRepository()
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model=settings.EMBEDDING_MODEL,
            )

    async def chat(self, question: str, project_id: str):

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        query_vector = self.embeddings.embed_query(question)

        semantic_results = self.qdrant_client.query_points(
            collection_name=project["name"],
            query=query_vector,
            limit=5,
            with_payload=True,
        )

        bm25_results = bm25_retriever.invoke(question)
        return result











            