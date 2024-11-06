"""
Asynchronous interface for interacting with plumbing API routes.

Clients can use these, but they are less user friendly than our higher level
APIs. They often act as the "plumbing" layer between higher-level APIs.
"""

__all__ = ["AsyncPlumbing"]

from fixpoint_common.types.extraction import (
    CreateRecordExtractionRequest,
    RecordExtraction,
)
from fixpoint_common.types.json_extraction import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
)
from fixpoint_common.types.parsing import (
    CreateCrawlUrlParseRequest,
    CrawlUrlParseResult,
    WebpageParseResult,
    CreateWebpageParseRequest,
)
from .._common.plumbing import (
    async_create_json_schema_extraction,
    async_create_question_answer_record_extraction,
    async_create_simple_crawl_url_parse,
    async_create_simple_webpage_parse,
)
from ._config import AsyncConfig


class AsyncPlumbing:
    """Asynchronous interface for plumbing API routes."""

    _config: AsyncConfig
    _extractions: "_AsyncPlumbingExtractions"
    _parses: "_AsyncPlumbingParses"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._extractions = _AsyncPlumbingExtractions(config)
        self._parses = _AsyncPlumbingParses(config)

    @property
    def extractions(self) -> "_AsyncPlumbingExtractions":
        """Async interface to extractions API routes."""
        return self._extractions

    @property
    def parses(self) -> "_AsyncPlumbingParses":
        """Async interface to parses API routes."""
        return self._parses


class _AsyncPlumbingExtractions:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create_json_schema_extraction(
        self, req: CreateJsonSchemaExtractionRequest
    ) -> JsonSchemaExtraction:
        """Create a structured JSON extraction from a data source asynchronously.

        Args:
            req (CreateJsonSchemaExtractionRequest): The request containing details for the
                extraction.

        Returns:
            JsonSchemaExtraction: The created extraction.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                extraction.
        """
        return await async_create_json_schema_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )

    async def create_question_answer_record_extraction(
        self, req: CreateRecordExtractionRequest
    ) -> RecordExtraction:
        """Create a question and answer ResearchRecord extraction asynchronously.

        Args:
            req (CreateRecordExtractionRequest): The request
                containing details for the extraction.

        Returns:
            RecordExtraction: The created extraction.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                extraction.
        """
        return await async_create_question_answer_record_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _AsyncPlumbingParses:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create_simple_webpage_parse(
        self, req: CreateWebpageParseRequest
    ) -> WebpageParseResult:
        """Create a simple webpage parse asynchronously.

        A simple webpage parse parses a single webpage URL and extracts
        LLM-ready markdown. The text is not chunked.
        """
        return await async_create_simple_webpage_parse(
            self._config.http_client,
            self._config.core,
            req,
        )

    async def create_simple_crawl_url_parse(
        self, req: CreateCrawlUrlParseRequest
    ) -> CrawlUrlParseResult:
        """Create a simple crawl url parse asynchronously.

        A simple crawl url parse crawls webpages starting from a given URL and
        extracts LLM-ready markdown from all the pages it can find at that URL.
        The parsed text is not chunked.
        """
        return await async_create_simple_crawl_url_parse(
            self._config.http_client,
            self._config.core,
            req,
        )
