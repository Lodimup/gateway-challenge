import json
from hashlib import md5

import httpx
from data.data_map import MOCK_DATA_MAP
from db.uploads import query_upload_by
from pydantic_core import Url
from scheduler import app
from tasks.interfaces import ITaskResponse


@app.task
def mock_ocr(url: Url, user_id: str) -> ITaskResponse:
    """
    Mock OCR
    - file must exist in the bucket before calling this function
    - Any arbitary url not from the bucket is denied
    """
    r = httpx.get(url)
    try:
        r.raise_for_status()
    except httpx.HTTPStatusError as _:
        ret = {
            "data": None,
            "error": {
                "status_code": 400,
                "detail": "invalid url",
            },
        }
        return ITaskResponse(**ret).model_dump()

    md5_hash = md5(r.content).hexdigest()
    if query_upload_by(md5=md5_hash, user_id=user_id) is None:
        ret = {
            "data": None,
            "error": {
                "status_code": 404,
                "detail": "File have not been uploaded yet",
            },
        }
        return ITaskResponse(**ret).model_dump()

    fp = MOCK_DATA_MAP.get(md5_hash)
    with open(fp, "r") as f:
        ret = {
            "data": json.load(f),
            "error": None,
        }

    return ITaskResponse(**ret).model_dump()
