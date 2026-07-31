import json

from fastapi import UploadFile

from app.clients.s3_client import S3Client
from app.repositories.docs.project_repository import ProjectRepository
from app.repositories.faq.faq_file_repository import FAQFileRepository
from app.services.faq.faq_indexing_service import FAQIndexingService
from app.services.faq.faq_log_service import FAQLogService
from app.schemas.faq.management import FAQFile, FAQItem
from app.schemas.faq.upload import FAQFileMetadata, FAQUploadItem
from app.schemas.faq.logging import FAQFileDeletedLogEntry
from app.services.faq.exceptions import (
    FAQFileAlreadyExistsError,
    FAQFileNotFoundError,
    InvalidFAQFileError,
    ProductNotFoundError,
)
from app.shared.ids import generate_faq_id, generate_timestamp
from app.schemas.faq.logging import FAQFileCreatedLogEntry, FAQFileDeletedLogEntry



class FAQFileService:
    def __init__(
        self,
        s3_client: S3Client,
        indexing_service: FAQIndexingService,
        file_repository: FAQFileRepository,
        project_repository: ProjectRepository,
        log_service: FAQLogService,
    ):
        self._s3 = s3_client
        self._indexing = indexing_service
        self._files = file_repository
        self._projects = project_repository
        self._log = log_service

    @staticmethod
    def _faq_key(key_base: str) -> str:
        return f"{key_base}/faq_{key_base}.json"

    async def _resolve_key_base(self, product_id: str) -> str:
        project = await self._projects.get_by_id(product_id)
        if project is None:
            raise ProductNotFoundError(f"Aucun produit trouvé pour l'id {product_id}")
        name = (project.get("name") or "").strip()
        return name if name else product_id

    @staticmethod
    def _parse_items(raw_bytes: bytes) -> list[FAQUploadItem]:
        try:
            payload = json.loads(raw_bytes)
        except json.JSONDecodeError as exc:
            raise InvalidFAQFileError("Le fichier n'est pas un JSON valide") from exc

        raw_items = payload.get("items") if isinstance(payload, dict) else payload
        if not isinstance(raw_items, list) or not raw_items:
            raise InvalidFAQFileError(
                "Le JSON doit être une liste d'items ou un objet {'items': [...]}"
            )
        try:
            return [FAQUploadItem.model_validate(item) for item in raw_items]
        except Exception as exc:
            raise InvalidFAQFileError(f"Item(s) invalide(s) : {exc}") from exc
        
    async def create_faq_file(
        self, product_id: str, file: UploadFile, admin: str
    ) -> FAQFileMetadata:
        key_base = await self._resolve_key_base(product_id)

        existing = await self._files.get_by_product(product_id)
        if existing is not None:
            raise FAQFileAlreadyExistsError(
                f"Un fichier FAQ existe déjà pour le produit {product_id}"
            )

        raw_bytes = await file.read()
        upload_items = self._parse_items(raw_bytes)

        items = [
            FAQItem(
                id=generate_faq_id(),
                category=upload_item.category,
                question=upload_item.question,
                answer=upload_item.answer,
            )
            for upload_item in upload_items
        ]
        faq_file = FAQFile(product_id=product_id, items=items)
        key = self._faq_key(key_base)
        filename = file.filename or "faq.json"

        # 1. Écriture S3
        self._s3.put_json(key, faq_file.model_dump())

        # 2. Indexation Qdrant — rollback S3 si échec
        try:
            await self._indexing.index_file(key_base, items)
        except Exception:
            await self._s3.delete_file(key)
            print(f"create_faq_file - échec indexation Qdrant, rollback S3 pour {product_id}")
            raise

        # 3. Metadata Mongo — rollback S3 + Qdrant si échec
        metadata = FAQFileMetadata(
            product_id=product_id,
            filename=filename,
            s3_key=key,
            admin=admin,
            item_count=len(items),
            created_at=generate_timestamp().isoformat(),
        )
        try:
            await self._files.insert(metadata)
        except Exception:
            await self._s3.delete_file(key)
            self._indexing.handle_file_deleted(key_base)
            print(f"create_faq_file - échec écriture Mongo, rollback S3+Qdrant pour {product_id}")
            raise

        # 4. Log — après succès complet, ne fait pas échouer la création si erreur log
        self._log.write(
            FAQFileCreatedLogEntry(
                product_id=product_id,
                admin=admin,
                timestamp=generate_timestamp(),
                filename=filename,
                item_count=len(items),
            )
        )

        return metadata

    async def get_faq_file(self, product_id: str) -> FAQFile:
        meta = await self._files.get_by_product(product_id)
        if meta is None:
            raise FAQFileNotFoundError(f"Aucun fichier FAQ pour le produit {product_id}")

        raw = self._s3.get_json(meta["s3_key"])
        if raw is None:
            raise FAQFileNotFoundError(f"Aucun fichier FAQ pour le produit {product_id}")
        return FAQFile.model_validate(raw)

    async def delete_faq_file(self, product_id: str, admin: str) -> None:
        """
        Supprime entièrement le fichier FAQ d'un produit : Mongo + S3 + Qdrant.
        Tout-ou-rien avec rollback en cascade.
        """
        meta_doc = await self._files.get_by_product(product_id)
        if meta_doc is None:
            raise FAQFileNotFoundError(f"Aucun fichier FAQ pour le produit {product_id}")

        metadata = FAQFileMetadata.model_validate(meta_doc)
        key = metadata.s3_key
        key_base = key.split("/")[0]

        # capture le contenu S3 pour un éventuel rollback
        previous_raw = self._s3.get_json(key)

        # 1. Suppression Mongo (rollback : réinsertion, opération bon marché)
        deleted = await self._files.delete_by_product(product_id)
        if not deleted:
            raise FAQFileNotFoundError(
                f"Aucun fichier FAQ pour le produit {product_id} (suppression concurrente ?)"
            )

        # 2. Suppression S3 (rollback : réinsertion Mongo + restauration du JSON)
        try:
            await self._s3.delete_file(key)
        except Exception:
            await self._files.insert(metadata)
            print(f"delete_faq_file - échec suppression S3, rollback Mongo pour {product_id}")
            raise

        # 3. Suppression Qdrant — dernière étape (rollback : réinsertion Mongo + restauration S3)
        try:
            self._indexing.handle_file_deleted(key_base)
        except Exception:
            await self._files.insert(metadata)
            if previous_raw is not None:
                self._s3.put_json(key, previous_raw)
            print(f"delete_faq_file - échec suppression Qdrant, rollback Mongo+S3 pour {product_id}")
            raise

        # 4. Log — après succès complet, ne fait pas échouer la suppression si erreur log
        self._log.write(
            FAQFileDeletedLogEntry(
                product_id=product_id,
                admin=admin,
                timestamp=generate_timestamp(),
                filename=metadata.filename,
                item_count=metadata.item_count,
            )
        )