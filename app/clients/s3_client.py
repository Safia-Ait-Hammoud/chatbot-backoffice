import json
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from app.core.config import Settings


class S3Client:
    def __init__(self, settings: Settings):
        self._bucket = settings.bucket_name
        self._client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def get_json(self, key: str) -> Optional[dict]:

        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code in ("NoSuchKey", "404"):
                return None
            raise
        body = response["Body"].read()
        return json.loads(body)

    def put_json(self, key: str, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )