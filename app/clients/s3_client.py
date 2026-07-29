import json
from typing import Optional
from pathlib import Path
from uuid import uuid4
import asyncio

import boto3
from botocore.exceptions import ClientError

from app.core.config import Settings

from fastapi import HTTPException, UploadFile




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




    async def upload_file(self, file: UploadFile, folder: str) -> dict:
        filename = Path(file.filename).name
        s3_key = f"{folder}/{uuid4()}_{filename}"
        url = f"https://{self._bucket}.s3.amazonaws.com/{s3_key}"

        try:
            await asyncio.to_thread(
                self._client.upload_fileobj,
                file.file,
                self._bucket,
                s3_key,
                ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
            )
        except ClientError as exc:
            raise RuntimeError(f"Erreur S3 (upload) : {exc}") from exc

        return {"filename": filename, "s3_key": s3_key, "url": url}

    async def download_file(self, s3_key: str) -> bytes:
        try:
            response = await asyncio.to_thread(
                self._client.get_object, Bucket=self._bucket, Key=s3_key
            )
            return response["Body"].read()
        except ClientError as exc:
            raise RuntimeError(f"Erreur S3 (download) : {exc}") from exc

    async def delete_file(self, s3_key: str) -> None:
        try:
            await asyncio.to_thread(
                self._client.delete_object, Bucket=self._bucket, Key=s3_key
            )
        except ClientError as exc:
            raise RuntimeError(f"Erreur S3 (delete) : {exc}") from exc
    