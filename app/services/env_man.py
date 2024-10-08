"""
This module is responsible for loading the environment variables,
and converting them to the correct type.
- Prevents the app from staring if the environment variables are not found.
- Ignored if the app is running in the build environment.
"""

import os
from typing import Any

ENV_NAMES = [
    "DEPLOYENV",  # build, dev, prod, test
    "DEBUG",
    "CELERY_BROKER",
    "CELERY_BACKEND",
    "CACHE_REDIS_HOST",
    "CACHE_REDIS_PORT",
    "CACHE_REDIS_DB",
    "CACHE_REDIS_PASSWORD",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_BUCKET_URL",
    "AWS_BUCKET_NAME",
    "AWS_ENDPOINT_URL",
    "MONGO_URI",
    "OPENAI_API_KEY",
    "PINECONE_API_KEY",
]

ENVS: dict[str, Any] = {}
errs: list[str] = []


def convert_env(env: str, value: str) -> Any:
    """Converts the environment variables to the correct type.

    Args:
        env (str): environment variable name
        value (str): environment variable value

    Returns:
        Any: converted value
    """
    match env:
        case "DEBUG":
            return value.lower() == "true"
        case _:
            return value


if os.environ.get("DEPLOYENV") not in ["build"]:
    for env in ENV_NAMES:
        try:
            ENVS[env] = convert_env(env, os.environ[env])
        except KeyError as e:
            errs.append(str(e).strip("'"))

    if errs:
        raise EnvironmentError(f'Envs not found: {", ".join(errs)}')
