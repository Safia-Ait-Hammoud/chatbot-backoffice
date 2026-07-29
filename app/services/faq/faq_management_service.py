from app.clients.s3_client import S3Client
from app.schemas.faq.indexingFaq import FAQCreatedEvent, FAQDeletedEvent, FAQUpdatedEvent
from app.services.faq.faq_indexing_service import FAQIndexingService
from app.schemas.faq.logging import (
    FAQCreatedLogEntry,
    FAQDeletedLogEntry,
    FAQUpdatedLogEntry,
    QAPair,
)
from app.services.faq.faq_log_service import FAQLogService
from app.schemas.faq.management import (
    FAQCreateRequest,
    FAQDeleteRequest,
    FAQFile,
    FAQItem,
    FAQUpdateRequest,
)
from app.shared.ids import generate_faq_id, generate_timestamp


class FAQNotFoundError(Exception):
    """Levée quand un faq_id n'existe pas dans le fichier FAQ du produit."""


class FAQManagementService:
    def __init__(
        self,
        s3_client: S3Client,
        log_service: FAQLogService,
        indexing_service: FAQIndexingService,
    ):
        self._s3 = s3_client
        self._log = log_service
        self._indexing = indexing_service

    @staticmethod
    def _faq_key(product_id: str) -> str:
        print(f"create_key : faq_{product_id}.json")
        return f"faq_{product_id}.json"

    def _load_faq_file(self, product_id: str) -> FAQFile:
         key = f"{product_id}/{self._faq_key(product_id)}"
         raw = self._s3.get_json(key)
         if raw is None:
            return FAQFile(product_id=product_id, items=[])
         print(f"load_faq_file - done")
         return FAQFile.model_validate(raw)
  
   

    def _save_faq_file(self, faq_file: FAQFile) -> None:
        key= f"{faq_file.product_id}/{self._faq_key(faq_file.product_id)}"
        self._s3.put_json(key, faq_file.model_dump(mode="json"))
        print("save_faq_file - faq_file")

    @staticmethod
    def _find_item(faq_file: FAQFile, faq_id: str) -> FAQItem:
        item = next((i for i in faq_file.items if i.id == faq_id), None)
        if item is None:
            raise FAQNotFoundError(
                f"FAQ {faq_id} introuvable pour le produit {faq_file.product_id}"
            )
        return item

   
    # Création
 
    def create_faq(self, product_id: str, request: FAQCreateRequest) -> FAQItem:
        faq_file = self._load_faq_file(product_id)

        faq_id = generate_faq_id()
        print(f"create_faq - faq_id: {faq_id}, product_id: {product_id}")
        new_item = FAQItem(
            id=faq_id,
            category=request.category,
            question=request.question,
            answer=request.answer,
        )
        faq_file.items.append(new_item)
        self._save_faq_file(faq_file)

        self._indexing.handle_created(
            FAQCreatedEvent(
                category=request.category,
                faq_id=faq_id,
                product_id=product_id,
                question=request.question,
                answer=request.answer,
            )
        )

        self._log.write(
                    FAQCreatedLogEntry(
                        faq_id=faq_id,
                        category=request.category,
                        product_id=product_id,
                        admin=request.admin,
                        timestamp=generate_timestamp(),
                        question=request.question,
                        answer=request.answer,
                    )
                )

        return new_item

  
    # Mise à jour
  
    def update_faq(self, product_id: str, faq_id: str, request: FAQUpdateRequest) -> FAQItem:
        faq_file = self._load_faq_file(product_id)
        item = self._find_item(faq_file, faq_id)

        before = QAPair(question=item.question, answer=item.answer)


        new_question = request.question if request.question is not None else item.question
        new_answer = request.answer if request.answer is not None else item.answer

        
        question_changed = new_question != item.question

        item.question = new_question
        item.answer = new_answer
        item.category = request.category if request.category is not None else item.category
        
        self._save_faq_file(faq_file)

       
        self._indexing.handle_updated(
            FAQUpdatedEvent(
                category=item.category,
                faq_id=faq_id,
                product_id=product_id,
                question=new_question,
                answer=new_answer,
                question_changed=question_changed,
            )
        )

        self._log.write(
                    FAQUpdatedLogEntry(
                        faq_id=faq_id,
                        product_id=product_id,
                        admin=request.admin,
                        timestamp=generate_timestamp(),
                        before=before,
                        after=QAPair(question=new_question, answer=new_answer),
                    )
            )
        

    

        return item

   
    # Suppression
    def delete_faq(self, product_id: str, faq_id: str, request: FAQDeleteRequest) -> None:
        faq_file = self._load_faq_file(product_id)
        item = self._find_item(faq_file, faq_id)  

        faq_file.items = [i for i in faq_file.items if i.id != faq_id]
        self._save_faq_file(faq_file)

        self._indexing.handle_deleted(FAQDeletedEvent(faq_id=faq_id, product_id=product_id))

        self._log.write(
                    FAQDeletedLogEntry(
                        faq_id=faq_id,
                        product_id=product_id,
                        admin=request.admin,
                        timestamp=generate_timestamp(),
                        question=item.question,
                        answer=item.answer,
                    )
                )