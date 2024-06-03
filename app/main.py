"""
FastAPI entrypoint see: README.md
"""

from fastapi import FastAPI
from routers import auths, healths, ocrs, users
from services import logs  # noqa
from services.env_man import ENVS

app = FastAPI(debug=ENVS["DEBUG"])
app.include_router(ocrs.router)
app.include_router(auths.router)
app.include_router(users.router)
app.include_router(healths.router)
