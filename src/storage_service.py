from typing import Any

from botocore.exceptions import ClientError


class StorageService:
    def __init__(self, s3_client: Any, bucket_name: str) -> None:
        self._s3 = s3_client
        self._bucket = bucket_name

    def upload_file(self, file_content: bytes, object_key: str) -> None:
        self._s3.put_object(Bucket=self._bucket, Key=object_key, Body=file_content)

    def download_file(self, object_key: str) -> bytes | None:
        try:
            response = self._s3.get_object(Bucket=self._bucket, Key=object_key)
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise

    def delete_file(self, object_key: str) -> None:
        self._s3.delete_object(Bucket=self._bucket, Key=object_key)

    def list_files(self) -> list[str]:
        response = self._s3.list_objects_v2(Bucket=self._bucket)
        return [obj["Key"] for obj in response.get("Contents", [])]

    def generate_download_url(self, object_key: str, expires_in: int = 300) -> str:
        return self._s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket, "Key": object_key},
            ExpiresIn=expires_in,
        )

    def ensure_bucket_exists(self) -> None:
        try:
            self._s3.head_bucket(Bucket=self._bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self._s3.create_bucket(Bucket=self._bucket)
            else:
                raise
