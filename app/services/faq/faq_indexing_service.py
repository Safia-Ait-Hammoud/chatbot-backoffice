from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantWrapper
from app.schemas.faq.indexingFaq import FAQCreatedEvent, FAQDeletedEvent, FAQUpdatedEvent
from qdrant_client.http import models as qmodels
from app.schemas.faq.management import FAQItem

class FAQIndexingService:
    def __init__(self, embedding_client: EmbeddingClient, qdrant_client: QdrantWrapper):
        self._embedding = embedding_client
        self._qdrant = qdrant_client

    def handle_created(self, event: FAQCreatedEvent) -> None:
        vector = self._embedding.generate(event.question)
        payload = {
            "question": event.question,
            "answer": event.answer,
            "product_id": event.product_id,
            "category": event.category
        }
        self._qdrant.insert(
            product_id=event.product_id,
            point_id=event.faq_id,
            vector=vector,
            payload=payload,
        )
        print(f"FAQIndexingService.handle_created - event: {event}")

    def handle_updated(self, event: FAQUpdatedEvent) -> None:
        payload = {
            "question": event.question,
            "answer": event.answer,
            "product_id": event.product_id,
            "category": event.category
        }
        if event.question_changed:
            vector = self._embedding.generate(event.question)
            self._qdrant.upsert(
                product_id=event.product_id,
                point_id=event.faq_id,
                vector=vector,
                payload=payload,
            )
        else:
            self._qdrant.update_payload(
                product_id=event.product_id,
                point_id=event.faq_id,
                payload=payload,
            )
            print(f"FAQIndexingService.handle_updated - event: {event}")

    def handle_deleted(self, event: FAQDeletedEvent) -> None:
        self._qdrant.delete(
            product_id=event.product_id,
            point_id=event.faq_id,
        )
        print(f"FAQIndexingService.handle_deleted - event: {event}")



    async def index_file(self, product_id: str, items: list[FAQItem]) -> None:
        """
        Indexe tous les items d'un coup (1 seul appel embedding batché).
        Utilisé lors de la création du fichier FAQ complet d'un produit.
        """
        if not items:
            return

        vectors = await self._embedding.generate_many([item.question for item in items])

        points = [
            qmodels.PointStruct(
                id=item.id,
                vector=vector,
                payload={
                    "question": item.question,
                    "answer": item.answer,
                    "product_id": product_id,
                    "category": item.category,
                },
            )
            for item, vector in zip(items, vectors)
        ]
        self._qdrant.insert_batch(product_id, points)
        print(f"FAQIndexingService.index_file - product_id: {product_id}, count: {len(points)}")

        

    def handle_file_deleted(self, product_id: str) -> None:
        """Rollback / suppression complète de l'index d'un produit."""
        self._qdrant.delete_collection(product_id)
        print(f"FAQIndexingService.handle_file_deleted - product_id: {product_id}")