"""Types for extraction requests and responses."""

__all__ = [
    "CreateRecordExtractionRequest",
    "RecordExtraction",
]

from typing import Optional, Union, List
from pydantic import BaseModel, Field

from fixpoint_common.completions import ChatCompletionMessageParam
from fixpoint_common.types.json_extraction import (
    JsonSchemaExtraction,
)
from .citations import Citation
from .research import ResearchRecord
from .sources import TextSource, WebpageSource, CrawlUrlSource, BatchTextSource
from .workflow import WorkflowId, WorkflowRunId


class CreateRecordExtractionRequest(BaseModel):
    """Request to create Record Q&A extraction."""

    document_id: Optional[str] = None
    document_name: Optional[str] = None
    workflow_id: WorkflowId
    run_id: Optional[WorkflowRunId] = None

    source: Union[
        CrawlUrlSource,
        WebpageSource,
        TextSource,
        BatchTextSource,
    ] = Field(description="The source of the data to extract.")

    extra_instructions: Optional[List[ChatCompletionMessageParam]] = Field(
        description="Additional prompt instructions",
        default=None,
    )

    questions: List[str] = Field(description="The questions to answer.")


class RecordExtraction(BaseModel):
    """Extraction result from a question and answer record extraction."""

    result_record: ResearchRecord = Field(
        description="The research record containing the extracted data."
    )
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    sub_json_extractions: List[JsonSchemaExtraction] = Field(
        description="The sub-extractions that resulted in this extraction."
    )
