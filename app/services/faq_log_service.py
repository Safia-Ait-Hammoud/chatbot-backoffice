
from app.clients.s3_client import S3Client
from app.schemas.faq.logging import FAQLogEntry
from app.shared.ids import format_timestamp_for_filename


class FAQLogService:
    def __init__(self, s3_client: S3Client):
        self._s3 = s3_client

    def write(self, entry: FAQLogEntry) -> None:
        ts_str = format_timestamp_for_filename(entry.timestamp)
        key = f"logs/{entry.product_id}/{ts_str}_{entry.faq_id}_{entry.action.value}.json"
        self._s3.put_json(key, entry.model_dump(mode="json"))
        print(f"FAQLogService.write - done")