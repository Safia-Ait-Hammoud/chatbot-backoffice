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





    def ensure_collection_raw(self, collection_name: str) -> None:
        """
        Crée la collection si elle n'existe pas, SANS préfixe.
        Le nom passé est utilisé tel quel (ex: nom du projet).
        """
        if not self._client.collection_exists(collection_name):
            self._client.create_collection(
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=qmodels.Distance.COSINE,
                ),
            )

    def upsert_points(self, collection_name: str, points: list[qmodels.PointStruct]) -> None:
        """
        Upsert de plusieurs points dans une collection déjà nommée
        (pas de préfixe appliqué).
        """
        self.ensure_collection_raw(collection_name)
        self._client.upsert(
            collection_name=collection_name,
            points=points,
        )

    def delete_by_filter(self, collection_name: str, filter_: qmodels.Filter) -> None:
        """
        Supprime tous les points correspondant à un filtre
        (ex: tous les chunks d'un document_id donné).
        """
        self._client.delete(
            collection_name=collection_name,
            points_selector=filter_,
        )


    def insert_batch(self, product_id: str, points: list[qmodels.PointStruct]) -> None:
        """Insertion en lot lors de la création du fichier FAQ d'un produit."""
        collection = self._ensure_collection(product_id)
        if points:
            self._client.upsert(collection_name=collection, points=points)

    def delete_collection(self, product_id: str) -> None:
        """Rollback : supprime la collection si une étape suivante échoue."""
        collection = self._collection_name(product_id)
        if self._client.collection_exists(collection):
            self._client.delete_collection(collection_name=collection)