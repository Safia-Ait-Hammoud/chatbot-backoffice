from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantWrapper
from app.schemas.faq.indexingFaq import FAQCreatedEvent, FAQDeletedEvent, FAQUpdatedEvent


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