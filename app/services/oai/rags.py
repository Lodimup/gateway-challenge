"""
Handles RAG related services
SEE: 
- https://openai.com/index/new-embedding-models-and-api-updates/
- https://platform.openai.com/docs/guides/embeddings/use-cases
"""

from typing import Literal

import nanoid
from openai import OpenAI
from openai.types.create_embedding_response import Embedding
from pinecone import Pinecone, ServerlessSpec
from services.env_man import ENVS

openai_client = OpenAI()
pinecone_client = Pinecone(api_key=ENVS["PINECONE_API_KEY"])


def create_index(
    name: str,
    dimension: int = 1536,
    metric: str = "cosine",
    spec: ServerlessSpec = ServerlessSpec(cloud="aws", region="us-east-1"),
) -> None:
    """
    Creates a Pinecone index
    text-embedding-3-small requires
    - 1536 dimensions
    - cosine metric
    Args:
        name (str): index name
        dimension (int): number of dimensions, defaults to 1536
        metric (str): metric type, defaults to "cosine"
        spec (ServerlessSpec): serverless spec, defaults to ServerlessSpec(cloud="aws", region="us-east-1")
    Returns:
        None
    Raises:
        pinecone.core.client.exceptions.PineconeApiException: (409) if the index already exists
    """
    return pinecone_client.create_index(name, dimension, spec, metric)


def get_embeddings(texts=list[str], model="text-embedding-3-small"):
    texts = [t.replace("\n", " ") for t in texts]
    return openai_client.embeddings.create(input=texts, model=model).data


def insert_embeddings(
    embeddings: list[Embedding],
    metadata: list[dict[str, str]],
    index: str,
    namespace: str = "default",
) -> dict[Literal["upserted_count"], int]:
    """
    Inserts embeddings into the Pinecone index
    Args:
        embeddings (list[Embedding]): embeddings to insert
        metadata (list[dict[str, str]]): metadata to insert
        index (str): index name
        namespace (str): namespace, defaults to "default"
    Returns:
        upsertResponse: ex. {"upserted_count": 2} if successful
    """
    index = pinecone_client.Index(index)
    vecters = []
    for i, e in enumerate(embeddings):
        payload = {
            "id": nanoid.generate(),
            "values": e["embedding"],
            "metadata": metadata[i],
        }
        vecters.append(payload)
    ret = index.upsert(
        vectors=vecters,
        namespace=namespace,
    )
    return ret.to_dict()


def query_embeddings(
    index: str,
    vector: list[float],
    top_k: int = 1,
    namespace: str = "default",
    include_values: bool = False,
    include_metadata: bool = True,
) -> dict:
    """
    Queries the Pinecone index
    Args:
        index (str): index name
        vector (list[float]): vector to query
        top_k (int): number of results to return, defaults to 1
        namespace (str): namespace, defaults to "default"
        include_values (bool): include values in the response, defaults to False
        include_metadata (bool): include metadata in the response, defaults to True
    Returns:
    {
        "matches": [
            {
                "id": "Weh1r9F-HYDyvEHy7eyYB",
                "metadata": {...},
                "score": 0.497888833,
                "values": [],
            },
            {
                "id": "HC1zTIICnP3NFEfFeNXf4",
                "metadata": {...},
                "score": 0.370420694,
                "values": [],
            },
            ...
        ],
        "namespace": "default",
        "usage": {"read_units": 6},
    }
    """

    index = pinecone_client.Index(index)
    ret = index.query(
        namespace=namespace,
        vector=vector,
        top_k=top_k,
        include_values=include_values,
        include_metadata=include_metadata,
    )
    return ret
