from typing import Literal

from pydantic import BaseModel
from pydantic_core import Url


class FileMeta(BaseModel):
    """
    id: id
    ext: file extension
    md5: md5
    filename: original filename
    url: cdn url
    user_id: owner's user id
    """

    id: str
    ext: str
    md5: str
    file_name: str
    url: Url
    user_id: str


class UploadPostOut(BaseModel):
    files: list[FileMeta]


class OcrPostIn(BaseModel):
    url: str
    user_id: str


class OcrPostOut(BaseModel):
    task_id: str


class OcrStatusGetOut(BaseModel):
    status: Literal[
        "PENDING",
        "STARTED",
        "RETRY",
        "FAILURE",
        "SUCCESS",
    ]
