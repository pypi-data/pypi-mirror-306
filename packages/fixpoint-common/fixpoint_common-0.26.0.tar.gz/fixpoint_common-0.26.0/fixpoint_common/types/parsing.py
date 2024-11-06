"""
Types for parsing web pages and other data sources into an LLM-ready format.
"""

__all__ = [
    "CreateWebpageParseRequest",
    "WebpageParseResult",
    "CreateCrawlUrlParseRequest",
    "CrawlUrlParseResult",
]


from typing import List, Optional

from pydantic import BaseModel, Field

from .sources import WebpageSource, CrawlUrlSource
from .workflow import WorkflowId, WorkflowRunId


class CreateWebpageParseRequest(BaseModel):
    """Request to parse a single webpage.

    Parses a webpage and returns the text (non-chunked) of the page. The output
    format is markdown.
    """

    source: WebpageSource
    workflow_id: WorkflowId
    run_id: Optional[WorkflowRunId]


# Parse results are called `...ParseResult` instead of `...Parse` because if we
# have a plain `CreateParseRequest`, returning a `Parse` object is confusing
# about whether that is a verb or a noun.


class WebpageParseResult(BaseModel):
    """A parse result from a single webpage.

    Contains the text (non-chunked) of the page. The output format is markdown.
    """

    source: WebpageSource
    content: str = Field(description="The parsed text, ready for LLM")


class CreateCrawlUrlParseRequest(BaseModel):
    """Request to start a crawl parse.

    Crawls webpages starting at a URL. Returns the text (non-chunked) per page.
    The output format is markdown.
    """

    source: CrawlUrlSource
    workflow_id: WorkflowId
    run_id: Optional[WorkflowRunId]


class CrawlUrlParseResult(BaseModel):
    """A parse result from crawling a URL.

    Contains the text (non-chunked) per page. The output format is markdown.
    """

    source: CrawlUrlSource
    page_contents: List[WebpageParseResult] = Field(
        description="The parsed contents of each page"
    )
