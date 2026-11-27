from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class S3ConnectionSettings(BaseModel):
    endpoint_url: str
    region_name: str
    access_key: str
    secret_key: str
    bucket_name: str


class S3ClientSettings(BaseModel):
    signature_version: str = "s3v4"
    addressing_style: str = "path"
    max_attempts: int = 3
    retry_mode: str = "standard"


class Settings(BaseSettings):
    minio: S3ConnectionSettings
    minio_client: S3ClientSettings = S3ClientSettings()

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
