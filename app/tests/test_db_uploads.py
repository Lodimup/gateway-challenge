from hashlib import md5
import nanoid
from db.uploads import IUploads, insert_upload, query_upload_by, set_ocr_status


def test_insert_upload():
    resp = insert_upload(
        IUploads(
            **{
                "id": nanoid.generate(),
                "ext": "pdf",
                "md5": str(md5()),
                "file_name": "file_name",
                "url": "url",
                "user_id": "user_id",
                "ocr_status": "NOT_STARTED",
                "schema_version": 1,
            }
        )
    )
    assert resp is True


def test_query_upload_by():
    md5_hash = str(md5())
    insert_upload(
        IUploads(
            **{
                "id": nanoid.generate(),
                "ext": "pdf",
                "md5": md5_hash,
                "file_name": "file_name",
                "url": "url",
                "user_id": "user_id",
                "ocr_status": "NOT_STARTED",
                "schema_version": 1,
            }
        )
    )
    resp = query_upload_by(md5=md5_hash)
    assert resp is not None


def test_set_ocr_status():
    md5_hash = str(md5())
    insert_upload(
        IUploads(
            **{
                "id": nanoid.generate(),
                "ext": "pdf",
                "md5": md5_hash,
                "file_name": "file_name",
                "url": "url",
                "user_id": "user_id",
                "ocr_status": "NOT_STARTED",
                "schema_version": 1,
            }
        )
    )
    resp = set_ocr_status(md5_hash, "user_id", "PENDING")
    assert resp is True
    resp = query_upload_by(md5=md5_hash)
    assert resp.ocr_status == "PENDING"
