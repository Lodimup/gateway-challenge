"""
Clients for databases
"""

import pymongo
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
