"""Common code for interacting with the plumbing API routes."""

__all__ = [
    "create_json_schema_extraction",
    "async_create_json_schema_extraction",
    "create_question_answer_record_extraction",
    "async_create_question_answer_record_extraction",
    "create_simple_crawl_url_parse",
    "async_create_simple_crawl_url_parse",
    "create_simple_webpage_parse",
    "async_create_simple_webpage_parse",
]

import os

import httpx

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
    CreateWebpageParseRequest,
    WebpageParseResult,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


_BASE_URL_PATH = "/plumbing"
_JSON_SCHEMA_EXTRACTIONS = os.path.join(
    _BASE_URL_PATH, "extractions", "json_schema_extractions"
)
_QUESTION_ANSWER_RECORD_EXTRACTIONS = os.path.join(
    _BASE_URL_PATH, "extractions", "question_answer_record_extractions"
)
_SIMPLE_CRAWL_URL_PARSES = os.path.join(
    _BASE_URL_PATH, "parses", "simple_crawl_url_parses"
)
_SIMPLE_WEBPAGE_PARSES = os.path.join(_BASE_URL_PATH, "parses", "simple_webpage_parses")


def create_json_schema_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a structured JSON extraction from a data source."""
    resp = http_client.post(
        config.route_url(_JSON_SCHEMA_EXTRACTIONS),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_json_schema_extraction_resp(resp)


async def async_create_json_schema_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a structured JSON extraction from a data source."""
    resp = await http_client.post(
        config.route_url(_JSON_SCHEMA_EXTRACTIONS),
        json=req.model_dump(),
    )
    # only raises if we got an error response
    return _process_json_schema_extraction_resp(resp)


def _process_json_schema_extraction_resp(resp: httpx.Response) -> JsonSchemaExtraction:
    # only raises if we got an error response
    raise_for_status(resp)
    return JsonSchemaExtraction.model_validate(resp.json())


def create_question_answer_record_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
) -> RecordExtraction:
    """Create a question and answer ResearchRecord extraction."""
    resp = http_client.post(
        config.route_url(_QUESTION_ANSWER_RECORD_EXTRACTIONS),
        json=req.model_dump(),
    )
    return _process_question_answer_record_extraction_resp(resp)


async def async_create_question_answer_record_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
) -> RecordExtraction:
    """Create a question and answer ResearchRecord extraction."""
    resp = await http_client.post(
        config.route_url(_QUESTION_ANSWER_RECORD_EXTRACTIONS),
        json=req.model_dump(),
    )
    return _process_question_answer_record_extraction_resp(resp)


def _process_question_answer_record_extraction_resp(
    resp: httpx.Response,
) -> RecordExtraction:
    raise_for_status(resp)
    return RecordExtraction.model_validate(resp.json())


####
# Parsing
####


async def async_create_simple_webpage_parse(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateWebpageParseRequest,
) -> WebpageParseResult:
    """Create an async simple webpage parse."""
    resp = await http_client.post(
        config.route_url(_SIMPLE_WEBPAGE_PARSES),
        json=req.model_dump(),
    )
    return _process_simple_webpage_parse_resp(resp)


def create_simple_webpage_parse(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateWebpageParseRequest,
) -> WebpageParseResult:
    """Create a simple webpage parse."""
    resp = http_client.post(
        config.route_url(_SIMPLE_WEBPAGE_PARSES),
        json=req.model_dump(),
    )
    return _process_simple_webpage_parse_resp(resp)


def _process_simple_webpage_parse_resp(
    resp: httpx.Response,
) -> WebpageParseResult:
    raise_for_status(resp)
    return WebpageParseResult.model_validate(resp.json())


def create_simple_crawl_url_parse(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateCrawlUrlParseRequest,
) -> CrawlUrlParseResult:
    """Create a simple crawl URL parse."""
    resp = http_client.post(
        config.route_url(_SIMPLE_CRAWL_URL_PARSES),
        json=req.model_dump(),
    )
    return _process_simple_crawl_url_parse_resp(resp)


async def async_create_simple_crawl_url_parse(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateCrawlUrlParseRequest,
) -> CrawlUrlParseResult:
    """Create an async simple crawl URL parse."""
    resp = await http_client.post(
        config.route_url(_SIMPLE_CRAWL_URL_PARSES),
        json=req.model_dump(),
    )
    return _process_simple_crawl_url_parse_resp(resp)


def _process_simple_crawl_url_parse_resp(
    resp: httpx.Response,
) -> CrawlUrlParseResult:
    raise_for_status(resp)
    return CrawlUrlParseResult.model_validate(resp.json())
