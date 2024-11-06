"""
Synchronous interface for parsing webpages and crawling URLs.
"""

__all__ = ["Parsing"]

from fixpoint_common.types.parsing import (
    CreateWebpageParseRequest,
    WebpageParseResult,
    CreateCrawlUrlParseRequest,
    CrawlUrlParseResult,
)
from .._common.parsing import create_webpage_parse, create_crawl_parse
from ._config import Config


class _WebpageParsing:
    """Synchronous interface for webpage parsing."""

    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateWebpageParseRequest) -> WebpageParseResult:
        """Parse a single webpage.

        Args:
            req (CreateWebpageParseRequest): The request containing details for the
                webpage parse.

        Returns:
            WebpageParseResult: The parsed webpage content.

        Raises:
            HTTPException: If there's an error in the HTTP request.
        """
        return create_webpage_parse(
            self._config.http_client,
            self._config.core,
            req,
        )


class _CrawlParsing:
    """Synchronous interface for crawl parsing."""

    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateCrawlUrlParseRequest) -> CrawlUrlParseResult:
        """Parse multiple webpages by crawling from a starting URL.

        Args:
            req (CreateCrawlUrlParseRequest): The request containing details for the
                crawl parse.

        Returns:
            CrawlUrlParseResult: The parsed contents from crawled pages.

        Raises:
            HTTPException: If there's an error in the HTTP request.
        """
        return create_crawl_parse(
            self._config.http_client,
            self._config.core,
            req,
        )


class Parsing:
    """Synchronous interface for webpage and crawl parsing."""

    _config: Config
    webpage: _WebpageParsing
    crawl: _CrawlParsing

    def __init__(self, config: Config):
        self._config = config
        self.webpage = _WebpageParsing(config)
        self.crawl = _CrawlParsing(config)
