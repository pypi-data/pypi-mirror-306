"""
Synchronous interface for interacting with extractions.
"""

__all__ = ["Extractions"]

from fixpoint_common.types import (
    CreateJsonSchemaExtractionRequest,
    JsonSchemaExtraction,
    CreateRecordExtractionRequest,
    RecordExtraction,
)
from .._common.extraction import (
    create_json_schema_extraction,
    create_record_extraction,
)
from ._config import Config


class Extractions:
    """Synchronous interface for JSON schema and Record extractions."""

    _config: Config
    _json: "_JsonSchemaExtraction"
    _record: "_RecordExtraction"

    def __init__(self, config: Config):
        self._config = config
        self._json = _JsonSchemaExtraction(config)
        self._record = _RecordExtraction(config)

    @property
    def json(self) -> "_JsonSchemaExtraction":
        """Sync interface to JSON schema extractions."""
        return self._json

    @property
    def record(self) -> "_RecordExtraction":
        """Sync interface to record extractions."""
        return self._record


class _JsonSchemaExtraction:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateJsonSchemaExtractionRequest) -> JsonSchemaExtraction:
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
        return create_json_schema_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )


class _RecordExtraction:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, req: CreateRecordExtractionRequest) -> RecordExtraction:
        """Create a record extraction."""
        return create_record_extraction(
            self._config.http_client,
            self._config.core,
            req,
        )
