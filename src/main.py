from client_factory import create_s3_client
from config import settings
from storage_service import StorageService


def main():
    minio_client = create_s3_client(
        s3_connection=settings.minio, s3_client_config=settings.minio_client
    )

    minio_service = StorageService(
        s3_client=minio_client, bucket_name=settings.minio.bucket_name
    )

    minio_service.ensure_bucket_exists()

    minio_service.upload_file(b"Hello, World!", "greetings/hello.txt")
    print("Файл загружен")

    files = minio_service.list_files()
    print(f"Файлы в бакете: {files}")

    content = minio_service.download_file("greetings/hello.txt")
    print(f"Скачанный контент: {content}")

    missing = minio_service.download_file("no-such-file.txt")
    print(f"Несуществующий файл вернул: {missing}")

    url = minio_service.generate_download_url("greetings/hello.txt")
    print(f"Presigned URL: {url}")


if __name__ == "__main__":
    main()
