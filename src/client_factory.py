from typing import Any, cast

import boto3
from botocore.config import Config

from config import S3ClientSettings, S3ConnectionSettings


def create_s3_client(
    s3_connection: S3ConnectionSettings, s3_client_cfg: S3ClientSettings
) -> Any:

    boto_config = Config(
        signature_version=s3_client_cfg.signature_version,
        s3=cast(Any, {"addressing_style": s3_client_cfg.addressing_style}),
        retries=cast(
            Any,
            {
                "max_attempts": s3_client_cfg.max_attempts,
                "mode": s3_client_cfg.retry_mode,
            },
        ),
    )

    return boto3.client(
        "s3",
        endpoint_url=s3_connection.endpoint_url,
        region_name=s3_connection.region_name,
        aws_access_key_id=s3_connection.access_key,
        aws_secret_access_key=s3_connection.secret_key,
        config=boto_config,
    )
