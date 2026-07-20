import asyncio
from pathlib import Path
from uuid import uuid4

from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

from core.aws import AWS_BUCKET_NAME, get_s3_client
from repositories.document_repository import DocumentRepository
from repositories.project_repository import ProjectRepository


class S3Service:

    def __init__(self):
        self.s3_client = get_s3_client()
        self.bucket_name = AWS_BUCKET_NAME
        self.document_repository = DocumentRepository()
        self.project_repository = ProjectRepository()

    async def upload_file(self, file: UploadFile, folder: str) -> dict:
        filename = Path(file.filename).name
        s3_key = f"{folder}/{uuid4()}_{filename}"
        url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"

        try:
            await asyncio.to_thread(
                self.s3_client.upload_fileobj,
                file.file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    "ContentType": file.content_type or "application/octet-stream"
                },
            )
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur S3 : {str(e)}"
            )

        return {
            "filename": filename,
            "s3_key": s3_key,
            "url": url
        }





    async def download_file(self, s3_key: str) -> bytes:
        try:
            response = await asyncio.to_thread(
                self.s3_client.get_object,
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response["Body"].read()
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur S3 (download) : {str(e)}"
            )





    async def delete_file(self, s3_key: str):
        try:
            await asyncio.to_thread(
                self.s3_client.delete_object,
                Bucket=self.bucket_name,
                Key=s3_key,
            )
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur S3 : {str(e)}"
            )