"""Types for the Fixpoint client and its APIs."""

__all__ = [
    "AllResearchResultsPydantic",
    "BatchTextSource",
    "Citation",
    "CrawlUrlSource",
    "CreateHumanTaskEntryRequest",
    "CreateJsonSchemaExtractionRequest",
    "CreateRecordExtractionRequest",
    "CreateResearchRecordRequest",
    "CreateCrawlUrlParseRequest",
    "CreateWebpageParseRequest",
    "Document",
    "HumanTaskEntry",
    "JsonSchemaExtraction",
    "ListDocumentsResponse",
    "ListHumanTaskEntriesResponse",
    "ListResearchRecordsResponse",
    "NodeStatus",
    "RecordExtraction",
    "ResearchField",
    "ResearchFieldEditableConfig",
    "ResearchRecord",
    "CrawlUrlParseResult",
    "WebpageParseResult",
    "Source",
    "TaskEntryField",
    "TaskFieldEditableConfig",
    "TextCitation",
    "TextSource",
    "WebPageCitation",
    "WebpageSource",
]

from fixpoint_common.types import Document, ListDocumentsResponse, NodeStatus
from fixpoint_common.types.human import (
    HumanTaskEntry,
    CreateHumanTaskEntryRequest,
    EntryField as TaskEntryField,
    EditableConfig as TaskFieldEditableConfig,
    ListHumanTaskEntriesResponse,
)
from fixpoint_common.types.research import (
    ResearchRecord,
    ResearchField,
    CreateResearchRecordRequest,
    ListResearchRecordsResponse,
    EditableConfig as ResearchFieldEditableConfig,
)
from fixpoint_common.webresearcher.types import AllResearchResultsPydantic
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
    CreateWebpageParseRequest,
    CrawlUrlParseResult,
    WebpageParseResult,
)
from fixpoint_common.types.sources import (
    TextSource,
    WebpageSource,
    CrawlUrlSource,
    BatchTextSource,
    Source,
)
from fixpoint_common.types.citations import Citation, TextCitation, WebPageCitation
