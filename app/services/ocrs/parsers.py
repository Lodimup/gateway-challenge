"""
Handles parsers for ocrs endpoints. Ensures that the OCR results are validated and ease of use.
"""

from collections import deque

from pydantic import BaseModel
from services.ocrs.utils import num_tokens_from_string


class Span(BaseModel):
    offset: int
    length: int


class BoundingRegion(BaseModel):
    pageNumber: int
    polygon: list[float]


class Paragraph(BaseModel):
    """
    Represents a paragraph in the OCR result
    """

    spans: list[Span]
    boundingRegions: list[BoundingRegion]
    content: str


class AnalyzeResult(BaseModel):
    """
    Represents the Analyze Result in the OCR result
    """

    apiVersion: str
    modelId: str
    stringIndexType: str
    content: str
    pages: list
    paragraphs: list[Paragraph]
    styles: list
    contentFormat: str


class OcrResult(BaseModel):
    """
    OCR Result Model for OCR results validation, and ease of use
    WARN: Unused fields are not typed
    """

    status: str
    createdDateTime: str
    lastUpdatedDateTime: str
    analyzeResult: AnalyzeResult

    @property
    def paragraph_content_len_min(self) -> int:
        """
        Returns the minimum length of the content of the paragraphs for analysis
        Returns:
            int: minimum length of the content of the paragraphs
        """
        return min([len(i.content) for i in self.analyzeResult.paragraphs])

    @property
    def paragraph_content_len_max(self) -> int:
        """
        Returns the maximum length of the content of the paragraphs for analysis
        Returns:
            int: maximum length of the content of the paragraphs
        """
        return max([len(i.content) for i in self.analyzeResult.paragraphs])

    @staticmethod
    def yield_paragraphs(
        queue: deque[Paragraph],
        max_token: int = 8000,
        encoding_name: str = "cl100k_base",
    ) -> list[Paragraph]:
        """
        Yields a list of Paragaph(s) from a queue that are less than, or equal to max_token.
        Construct the queue with deque(OcrResult.AnalyzeResult.Paragraphs).
        Use this to construct a list of Paragraph(s) to be vectorized.
        The OpenAI's max token is 8191.
        WARN: Mutates the queue
        Args:
            queue (deque[Paragraph]): a queue of Paragraph(s)
            max_token (int): maximum token length
            encoding_name (str): encoding name
        Returns:
            list[Paragraph]: list of Paragraph(s) that are less than or equal to max_token
        """
        total_tokens = 0
        result = []
        while queue:
            paragraph = queue.popleft()
            token_count = num_tokens_from_string(paragraph.content, encoding_name)
            if total_tokens + token_count > max_token:
                queue.appendleft(paragraph)
                break
            total_tokens += token_count
            result.append(paragraph)

        return result
