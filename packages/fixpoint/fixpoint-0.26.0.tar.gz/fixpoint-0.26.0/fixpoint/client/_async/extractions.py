"""
Asynchronous interface for interacting with extractions.
"""

__all__ = ["AsyncExtractions"]

from fixpoint_common.types import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
    CreateRecordExtractionRequest,
    RecordExtraction,
)
from .._common.extraction import (
    async_create_json_schema_extraction,
    async_create_record_extraction,
)
from ._config import AsyncConfig


class AsyncExtractions:
    """Asynchronous interface for JSON schema and Record extractions."""

    _config: AsyncConfig
    _json: "_AsyncJsonSchemaExtraction"
    _record: "_AsyncRecordExtraction"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._json = _AsyncJsonSchemaExtraction(config)
        self._record = _AsyncRecordExtraction(config)

    @property
    def json(self) -> "_AsyncJsonSchemaExtraction":
        """Async interface to JSON schema extractions."""
        return self._json

    @property
    def record(self) -> "_AsyncRecordExtraction":
        """Async interface to record extractions."""
        return self._record


class _AsyncJsonSchemaExtraction:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(
        self, req: CreateJsonSchemaExtractionRequest
    ) -> JsonSchemaExtraction:
        """Create a JSON schema extraction.

        Args:
            req (CreateJsonSchemaExtractionRequest): The request containing details for the
                JSON schema extraction.

        Returns:
            JsonSchemaExtraction: The created JSON schema extraction.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                research record.
        """
        return await async_create_json_schema_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _AsyncRecordExtraction:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, req: CreateRecordExtractionRequest) -> RecordExtraction:
        """Create a record extraction."""
        return await async_create_record_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )
