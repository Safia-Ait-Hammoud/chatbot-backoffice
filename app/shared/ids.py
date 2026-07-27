import uuid
from datetime import datetime, timezone


def generate_faq_id() -> str:

    return str(uuid.uuid4())


def generate_timestamp() -> datetime:
   
    return datetime.now(timezone.utc)


def format_timestamp_for_filename(ts: datetime) -> str:
    return ts.strftime("%Y%m%dT%H%M%S%f") + "Z"