"""
Test cases for tasks.ocrs
"""

import pytest
from tasks.ocrs import mock_ocr_and_embed_to_pc


@pytest.mark.skip(reason="Expensive test.")
def test_mock_ocr_success():
    """
    Test mock_ocr success
    """
    url = "https://bucket-dev.lodimup.com/bucket-dev/tektome/uploads/9TMF2cDwGHg1yAz3aNtg_.pdf"
    user_id = "czRvNxms7BeqfbBFWhM_r"
    r = mock_ocr_and_embed_to_pc.s(url, user_id).delay().get()
    assert r["data"] is not None
    assert r["error"] is None


@pytest.mark.skip(reason="Expensive test.")
def test_mock_ocr_failure():
    """
    Test mock_ocr failure due to invalid url
    """
    url = "https://bucket-dev.lodimup.com/bucket-dev/tektome/uploads/1234.pdf"
    user_id = "czRvNxms7BeqfbBFWhM_r"
    r = mock_ocr_and_embed_to_pc.s(url, user_id).delay().get()
    assert r["data"] is None
    assert r["error"] is not None
