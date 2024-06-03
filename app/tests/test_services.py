"""
Tests for services module.
"""

from services.storages import get_signed_url


def test_get_signed_url():
    bucket = "bucket"
    key = "key"
    expires_in = 3600

    result = get_signed_url(bucket, key, expires_in)

    assert isinstance(result, str)
