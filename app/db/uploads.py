"""
Handles upload collections
"""

from typing import Literal

from db.clients import get_mongo_db
from pydantic import BaseModel


class IUploads(BaseModel):
    """
    Uploads schema, prevents incorrect data from being inserted
    id: id
    ext: file extension
    md5: md5
    filename: original filename
    url: cdn url
    user_id: owner's user id
    ocr_status: ocr status
    schema_version: schema version number for future changes
    """

    id: str
    ext: str
    md5: str
    file_name: str
    url: str
    user_id: str
    ocr_status: Literal["NOT_STARTED", "PENDING", "SUCCESS"] = "NOT_STARTED"
    schema_version: int


def insert_upload(p: IUploads) -> bool:
    """
    Insert an upload record
    Args:
        p (IUploads): upload record
    Returns:
        bool: True if successful
    """
    uploads_col = get_mongo_db()["uploads"]
    uploads_col.insert_one(p.model_dump())

    return True


def query_upload_by(**kwargs) -> IUploads | None:
    """
    Get an upload record by query params
    Args:
        **kwargs: query params, see IUploads
    Returns:
        IUploads: upload record, None if not found
    """
    uploads_col = get_mongo_db()["uploads"]
    row = uploads_col.find_one(kwargs)
    if row is None:
        return None

    return IUploads(**row)


def set_ocr_status(
    md5: str,
    user_id: str,
    status: Literal["NOT_STARTED", "PENDING", "SUCCESS"],
) -> bool:
    """
    Set the ocr status of an upload record
    Args:
        md5 (str): md5 hash
        user_id (str): user id
        status (Literal["NOT_STARTED", "PENDING", "SUCCESS"]): ocr status
    Returns:
        bool: True if successful
    """
    uploads_col = get_mongo_db()["uploads"]
    uploads_col.update_one(
        {"md5": md5, "user_id": user_id},
        {"$set": {"ocr_status": status}},
    )

    return True
