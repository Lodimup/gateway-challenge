# Extras
Explains rationale behind some design decisions, and other useful information.

## DB
### MongoDB
MongoDB is used as metadata store. Since there is no complex queries, and the data is not relational, MongoDB is a good choice. It is also easy to scale, and has good performance. If the data was relational, and had complex queries, a SQL database would have been a better choice. 

## Packages
### nanoid
For unique IDS. Nanoid is used instead of UUID4 for generating unique IDs, nanoid is url-ready while UUID4 must be converted to web-safe base64 back, and forth. Collions probablity is similar. Nanoid is also faster.
```Python
from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID


def uuid2slug(uuidstring: str | UUID) -> str:
    """
    Convert a UUID to a slug.
    """
    return urlsafe_b64encode(UUID(str(uuidstring)).bytes).rstrip(b"=").decode("ascii")


def slug2uuid(slug: str) -> str:
    """
    Convert a slug to a UUID string.
    """
    return str(UUID(bytes=urlsafe_b64decode(str(slug) + "==")))


def slugify(s: str | UUID, decode: bool = False) -> str:
    """encode uuid to slug or decode slug to uuid

    Args:
        s (str): string to slugify / deslugify
        decode (bool, optional): to decode or encode. Defaults to False.

    Returns:
        str: slugified / deslugified string
    """
    if decode:
        return slug2uuid(s)  # type: ignore

    return uuid2slug(s)
```