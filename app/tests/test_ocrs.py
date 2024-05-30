"""
Test cases for tasks.ocrs
"""

from tasks.ocrs import ocr


def test_ocr():
    assert ocr(1, 2) == 3
