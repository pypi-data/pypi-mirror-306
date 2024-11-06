"""
Common extraction functions.
"""

__all__ = [
    "async_create_json_schema_extraction",
    "create_json_schema_extraction",
    "async_create_record_extraction",
    "create_record_extraction",
]

import httpx

from fixpoint_common.types import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
    CreateRecordExtractionRequest,
    RecordExtraction,
)
from fixpoint.errors import raise_for_status
from .core import ApiCoreConfig


_EXTRACTION_ROUTE = "/extractions"
_JSON_EXTRACTION_ROUTE = f"{_EXTRACTION_ROUTE}/json_schema_extractions"
_RECORD_EXTRACTION_ROUTE = f"{_EXTRACTION_ROUTE}/record_extractions"


async def async_create_json_schema_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a JSON schema extraction."""
    resp = await http_client.post(
        config.route_url(_JSON_EXTRACTION_ROUTE),
        # without `by_alias=True`, the `schema` field is serialized as
        # `schema_`
        json=req.model_dump(by_alias=True),
    )
    return _process_json_schema_extraction_resp(resp)


def create_json_schema_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateJsonSchemaExtractionRequest,
) -> JsonSchemaExtraction:
    """Create a JSON schema extraction."""
    resp = http_client.post(
        config.route_url(_JSON_EXTRACTION_ROUTE),
        # without `by_alias=True`, the `schema` field is serialized as
        # `schema_`
        json=req.model_dump(by_alias=True),
    )
    return _process_json_schema_extraction_resp(resp)


def _process_json_schema_extraction_resp(resp: httpx.Response) -> JsonSchemaExtraction:
    raise_for_status(resp)
    return JsonSchemaExtraction.model_validate(resp.json())


async def async_create_record_extraction(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
) -> RecordExtraction:
    """Create a record extraction."""
    resp = await http_client.post(
        config.route_url(_RECORD_EXTRACTION_ROUTE),
        json=req.model_dump(),
    )
    return _process_record_extraction_resp(resp)


def create_record_extraction(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateRecordExtractionRequest,
) -> RecordExtraction:
    """Create a record extraction."""
    resp = http_client.post(
        config.route_url(_RECORD_EXTRACTION_ROUTE),
        json=req.model_dump(),
    )
    return _process_record_extraction_resp(resp)


def _process_record_extraction_resp(resp: httpx.Response) -> RecordExtraction:
    raise_for_status(resp)
    return RecordExtraction.model_validate(resp.json())
