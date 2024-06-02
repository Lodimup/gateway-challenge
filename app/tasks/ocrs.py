import json
from collections import deque
from hashlib import md5

import httpx
from data.data_map import MOCK_DATA_MAP
from db.uploads import query_upload_by, set_ocr_status
from pydantic_core import Url
from scheduler import app
from services.oai.rags import get_embeddings, insert_embeddings
from services.ocrs.parsers import OcrResult, Paragraph
from tasks.interfaces import ITaskResponse


@app.task
def mock_ocr_and_embed_to_pc(url: Url, user_id: str) -> ITaskResponse:
    """
    Mock OCR and Embed to Pinecone
    Celery task cannot return non-json serializable objects.
    We return dict here, but we still do type checks.
    - file must exist in the bucket before calling this function
    - Any arbitary url not from the bucket is denied
    - If the file is not uploaded yet, return 404
    - If the file is uploaded, mock the ocr result and embed to Pinecone
    - When embedding, we chunk the paragraphs into chunks of less than 8000 tokens
    then batch embed
    - vector, and metadata are inserted into Pinecone
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
    upload = query_upload_by(md5=md5_hash, user_id=user_id)
    if upload is None:
        ret = {
            "data": None,
            "error": {
                "status_code": 404,
                "detail": "File have not been uploaded yet",
            },
        }
        return ITaskResponse(**ret).model_dump()
    if upload and upload.ocr_status != "NOT_STARTED":
        ret = {
            "data": None,
            "error": {
                "status_code": 400,
                "detail": "OCR already done, or in progress",
            },
        }
        return ITaskResponse(**ret).model_dump()
    set_ocr_status(md5_hash, user_id, "PENDING")

    fp = MOCK_DATA_MAP.get(md5_hash)
    with open(fp, "r") as f:
        ocr_result = OcrResult(**json.load(f))

    queue = deque(ocr_result.analyzeResult.paragraphs)

    # seperate paragraphs into chunks of less than 8000 tokens
    # TODO: optimization, each bundle can be sent to a different worker to parallelize
    # but it is out of scope right now
    bundled_paragraphs: list[Paragraph] = []
    while queue:
        bundled_paragraphs.append(OcrResult.yield_paragraphs(queue))
    for bundle in bundled_paragraphs:
        contents = [p.content for p in bundle]
        metadata = []
        for p in bundle:
            p: Paragraph
            meta = {
                "user_id": user_id,
                "md5_hash": md5_hash,
                "meta": p.model_dump_json(),
            }
            metadata.append(meta)
        vectors = get_embeddings(contents)
        vectors = [v.model_dump() for v in vectors]
        data = insert_embeddings(
            vectors,
            metadata,
            index="default",
            namespace="default",
        )
    set_ocr_status(md5_hash, user_id, "SUCCESS")
    return ITaskResponse(data=data, error=None).model_dump()
