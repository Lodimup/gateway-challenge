"""
FastAPI entrypoint see: README.md
"""

from fastapi import FastAPI
from routers import auths, healths, ocrs, users
from services import logs  # noqa
from services.env_man import ENVS

description = """
This is a serverless deployment of the Gateway Challenge.
Files are alrady uploaded to S3, and embeded to Pinecone.
OCR endpoints disallows OCR, and embedding if it has already been done.
If you need to re-OCR and re-embed, please notify me to clear the db.
Files with MD5 hashes not in the sample will be denied.
You may test uploading files, extractions, and other routes
"""

app = FastAPI(
    debug=ENVS["DEBUG"],
    description=description,
)
app.include_router(ocrs.router)
app.include_router(auths.router)
app.include_router(users.router)
app.include_router(healths.router)
