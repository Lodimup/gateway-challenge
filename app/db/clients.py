"""
Clients for databases
"""

import pymongo
from redis import Redis
from services.env_man import ENVS


def get_mongo_db(db: str = "mongo") -> pymongo.MongoClient:
    """
    Get a mongo client
    Args:
        db (str, optional): database name. Defaults to "mongo".
    Returns:
        pymongo.MongoClient: mongo client
    """
    client = pymongo.MongoClient(ENVS["MONGO_URI"])

    return client["mongo"]


rdb = Redis(
    host=ENVS["CACHE_REDIS_HOST"],
    port=ENVS["CACHE_REDIS_PORT"],
    db=ENVS["CACHE_REDIS_DB"],
    decode_responses=True,
)
