"""Live research and scraping tools wired to Tavily and Firecrawl.

Keys are read from the environment at call time so the tools degrade gracefully
when a key is absent — the agent receives an explanatory string and continues
with whatever context it already has.
"""

from __future__ import annotations

import os
from typing import List, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Tavily
# ---------------------------------------------------------------------------

class _TavilyQuery(BaseModel):
    query: str = Field(description="Search query to look up")


class TavilySearchTool(BaseTool):
    name: str = "Tavily Web Search"
    description: str = (
        "Search the web for current information about companies, industries, "
        "compliance news, job postings, and business intelligence. "
        "Returns title, URL, and content snippets for up to 5 results."
    )
    args_schema: Type[BaseModel] = _TavilyQuery

    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "TAVILY_API_KEY not set — skipping web search."
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=api_key)
            response = client.search(query=query, max_results=5)
            results = response.get("results") or []
            if not results:
                return "No results found."
            return "\n\n".join(
                f"**{r.get('title', 'Untitled')}**\n{r.get('url', '')}\n{r.get('content', '')}".strip()
                for r in results
            )
        except Exception as exc:
            return f"Tavily search error: {exc}"


# ---------------------------------------------------------------------------
# Firecrawl — scrape single URL
# ---------------------------------------------------------------------------

class _ScrapeInput(BaseModel):
    url: str = Field(description="Full URL of the page to scrape")


class FirecrawlScrapeTool(BaseTool):
    name: str = "Firecrawl Website Scrape"
    description: str = (
        "Fetch a URL and return its full content as clean markdown. "
        "Use for company websites, about/team pages, compliance pages, "
        "government contractor pages, and job postings."
    )
    args_schema: Type[BaseModel] = _ScrapeInput

    def _run(self, url: str) -> str:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "FIRECRAWL_API_KEY not set — skipping website scrape."
        try:
            from firecrawl import FirecrawlApp
            app = FirecrawlApp(api_key=api_key)
            result = app.scrape_url(url, formats=["markdown"])
            # firecrawl-py v1 returns an object with a .markdown attribute;
            # fall back to dict access for older builds.
            markdown = (
                getattr(result, "markdown", None)
                or (result.get("markdown") if isinstance(result, dict) else None)
                or ""
            )
            return markdown.strip() or "No content extracted from page."
        except Exception as exc:
            return f"Firecrawl scrape error: {exc}"


# ---------------------------------------------------------------------------
# Firecrawl — web search with full-page content
# ---------------------------------------------------------------------------

class _SearchInput(BaseModel):
    query: str = Field(description="Search query")
    limit: int = Field(default=5, description="Maximum number of results to return")


class FirecrawlSearchTool(BaseTool):
    name: str = "Firecrawl Web Search"
    description: str = (
        "Search the web and return full scraped content from matching pages. "
        "Prefer over Tavily when you need the complete page text, not just a snippet."
    )
    args_schema: Type[BaseModel] = _SearchInput

    def _run(self, query: str, limit: int = 5) -> str:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "FIRECRAWL_API_KEY not set — skipping web search."
        try:
            from firecrawl import FirecrawlApp
            app = FirecrawlApp(api_key=api_key)
            raw = app.search(query, limit=limit)
            # v1 may return a SearchResponse object or a plain list
            results: list = (
                raw if isinstance(raw, list)
                else getattr(raw, "data", None)
                or (raw.get("data") if isinstance(raw, dict) else None)
                or []
            )
            if not results:
                return "No results found."
            parts = []
            for r in results:
                if isinstance(r, dict):
                    title = r.get("title", "Untitled")
                    url = r.get("url", "")
                    body = r.get("markdown") or r.get("description") or ""
                else:
                    title = getattr(r, "title", "Untitled")
                    url = getattr(r, "url", "")
                    body = getattr(r, "markdown", None) or getattr(r, "description", "") or ""
                parts.append(f"**{title}**\n{url}\n{body}".strip())
            return "\n\n".join(parts)
        except Exception as exc:
            return f"Firecrawl search error: {exc}"


# ---------------------------------------------------------------------------
# Tool-set factories
# ---------------------------------------------------------------------------

def get_research_tools() -> List[BaseTool]:
    """Full research suite: Tavily search + Firecrawl scrape + Firecrawl search."""
    return [TavilySearchTool(), FirecrawlScrapeTool(), FirecrawlSearchTool()]


def get_enrichment_tools() -> List[BaseTool]:
    """Lighter enrichment suite: Tavily search + Firecrawl scrape."""
    return [TavilySearchTool(), FirecrawlScrapeTool()]
