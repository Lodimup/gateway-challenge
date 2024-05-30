import logging
from typing import IO, Union
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
import nanoid
from db.uploads import IUploads, insert_upload
from serializers.ocrs import FileMeta
from services.env_man import ENVS
from hashlib import md5


def upload_file(bucket: str, key: str, f: IO) -> bool:
    """
    Upload a file to an S3 bucket
    Args:
        bucket: Bucket to upload to
        key: S3 object name ex. "path/sample.pdf"
        f: File to upload
    """
    client = boto3.client("s3")
    try:
        client.put_object(Bucket=bucket, Key=key, Body=f)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def gen_file_url(bucket: str, key: str) -> str:
    """
    Generate a public file url
    Args:
        bucket: Bucket name
        key: S3 object name
    """
    bucket_url = ENVS["AWS_BUCKET_URL"]

    return f"{bucket_url}/{bucket}/{key}"


def handle_file_upload(
    f: UploadFile,
    user_id: str,
    namespace: str = "tektome/uploads",
) -> Union[FileMeta, False]:
    """
    Handles file upload
    - Calculate the md5 hash of the file
    - Upload the file to S3
    - Store file's metadata in mongodb
    Args:
        f: File to upload
        user_id: Owner's user id
        namespace: namespace ex sub.domain.tld/<namespace>/<file_id>.<ext>
    Returns:
        FileMeta | False: File metadata or False if failed
    """
    file_id = nanoid.generate()
    md5_hash = md5(f.file.read()).hexdigest()
    file_name = f.filename
    ext = file_name.split(".")[-1]
    key = f"{namespace}/{file_id}.{ext}"

    try:
        f.file.seek(0)
        upload_file(ENVS["AWS_BUCKET_NAME"], key, f.file)
    except Exception as e:
        logging.error(e)
        return False

    db_payload = IUploads(
        id=file_id,
        ext=ext,
        md5=md5_hash,
        file_name=file_name,
        url=gen_file_url(ENVS["AWS_BUCKET_NAME"], key),
        user_id=user_id,
        schema_version=1,
    )
    insert_upload(db_payload)
    ret = FileMeta(**db_payload.model_dump())

    return ret
