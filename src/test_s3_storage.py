import requests
from boto3 import client
from botocore.config import Config


def test_s3_workflow():
    s3 = client(
        's3',
        endpoint_url="http://localhost:5000",
        region_name="us-east-1",
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
        config=Config(signature_version="s3v4")
    )

    s3.create_bucket(Bucket='my-first-bucket')

    s3.put_object(
        Bucket='my-first-bucket',
        Key='documents/report.txt',
        Body=b"Quarterly report"
    )
    s3.put_object(
        Bucket='my-first-bucket',
        Key='images/logo.png',
        Body=b"fake-png-bytes"
    )

    response = s3.list_objects_v2(Bucket='my-first-bucket')
    keys = {obj['Key'] for obj in response['Contents']}
    assert len(keys) == 2, 'Error! There should be two keys.'
    assert keys == {'documents/report.txt', 'images/logo.png'}, f"Error! Expected two keys, got: {keys}"

    response = s3.get_object(Bucket='my-first-bucket', Key='documents/report.txt')
    assert response['Body'].read() == b"Quarterly report", "Error! Report content mismatch."

    s3.delete_object(Bucket='my-first-bucket', Key='images/logo.png')

    response = s3.list_objects_v2(Bucket='my-first-bucket')
    assert response['Contents'][0]['Key'] == 'documents/report.txt', 'Error! There should be one key.'

    tmp_url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {
            'Bucket': 'my-first-bucket',
            'Key': 'documents/report.txt'
        },
        ExpiresIn=300
    )

    response = requests.get(tmp_url)
    assert response.status_code == 200, 'Error! The response status code was not 200.'
    assert response.content == b"Quarterly report", "Error! Report content mismatch."