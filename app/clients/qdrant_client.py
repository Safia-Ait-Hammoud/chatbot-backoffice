from typing import Any

from qdrant_client import QdrantClient as _QdrantClient
from qdrant_client.http import models as qmodels

from app.core.config import Settings


class QdrantWrapper:

    VECTOR_SIZE = 3072
    COLLECTION_PREFIX = "faq_"

    def __init__(self, settings: Settings):
        self._client = _QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def _collection_name(self, product_id: str) -> str:
        return f"{self.COLLECTION_PREFIX}{product_id}"

    def _ensure_collection(self, product_id: str) -> str:
        collection = self._collection_name(product_id)
        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection_name=collection,
                vectors_config=qmodels.VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        return collection

    def insert(self, product_id: str, point_id: str, vector: list[float], payload: dict[str, Any]) -> None:
        """Insertion d'un nouveau point (cas 'created')."""
        collection = self._ensure_collection(product_id)
        self._client.upsert(
            collection_name=collection,
            points=[qmodels.PointStruct(id=point_id, vector=vector, payload=payload)],
        )

    def upsert(self, product_id: str, point_id: str, vector: list[float], payload: dict[str, Any]) -> None:
        """
        Upsert d'un point existant (cas 'updated' avec question_changed=True)
        """
        self.insert(product_id, point_id, vector, payload)

    def update_payload(self, product_id: str, point_id: str, payload: dict[str, Any]) -> None:
        """
        Met à jour uniquement le payload d'un point existant, sans régénérer
        le vecteur (cas 'updated' avec question_changed=False).
        """
        collection = self._ensure_collection(product_id)
        self._client.set_payload(
            collection_name=collection,
            payload=payload,
            points=[point_id],
        )

    def delete(self, product_id: str, point_id: str) -> None:
        """Suppression définitive d'un point (cas 'deleted')."""
        collection = self._collection_name(product_id)
        self._client.delete(
            collection_name=collection,
            points_selector=qmodels.PointIdsList(points=[point_id]),
        )

    def search(self, product_id: str, vector: list[float], limit: int = 5):
        """Recherche sémantique dans la collection isolée du produit"""
        collection = self._collection_name(product_id)
        return self._client.query_points(
            collection_name=collection,
            query=vector,
            limit=limit,
        )