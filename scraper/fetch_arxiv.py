"""Polite, retrying client for the official arXiv Atom API."""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any

import feedparser
import requests

from scraper.metadata import entry_to_paper
from scraper.utils import parse_datetime

LOGGER = logging.getLogger(__name__)
API_URL = "https://export.arxiv.org/api/query"


class ArxivRetrievalError(RuntimeError):
    """Raised when every configured query family fails."""


def _request_page(query: str, start: int, page_size: int, settings: dict[str, Any]) -> Any:
    params = {
        "search_query": query,
        "start": start,
        "max_results": page_size,
        "sortBy": "lastUpdatedDate",
        "sortOrder": "descending",
    }
    headers = {"User-Agent": settings["user_agent"]}
    last_error: Exception | None = None
    for attempt in range(1, settings["max_retries"] + 1):
        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=settings["request_timeout_seconds"])
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            if getattr(feed, "bozo", False) and not getattr(feed, "entries", []):
                raise ValueError(f"Malformed arXiv response: {feed.bozo_exception}")
            return feed
        except (requests.RequestException, ValueError) as error:
            last_error = error
            if attempt < settings["max_retries"]:
                delay = settings["retry_backoff_seconds"] * (2 ** (attempt - 1))
                LOGGER.warning("arXiv request failed (attempt %d/%d): %s; retrying in %ss",
                               attempt, settings["max_retries"], error, delay)
                time.sleep(delay)
    raise ArxivRetrievalError(str(last_error))


def fetch_query_family(name: str, query: str, cutoff: datetime, settings: dict[str, Any]) -> list[dict[str, Any]]:
    papers: list[dict[str, Any]] = []
    maximum = settings["max_results_per_query"]
    page_size = min(settings.get("page_size", 50), maximum)
    start = 0
    while start < maximum:
        requested = min(page_size, maximum - start)
        feed = _request_page(query, start, requested, settings)
        entries = list(getattr(feed, "entries", []))
        if not entries:
            break
        page_has_recent = False
        for entry in entries:
            try:
                paper = entry_to_paper(entry)
                updated = parse_datetime(paper["updated"])
                if updated and updated >= cutoff:
                    paper["matched_query_families"] = [name]
                    papers.append(paper)
                    page_has_recent = True
            except (KeyError, TypeError, ValueError) as error:
                LOGGER.warning("Skipping malformed arXiv entry in %s: %s", name, error)
        start += len(entries)
        if len(entries) < requested or not page_has_recent:
            break
        if start < maximum:
            time.sleep(settings["request_delay_seconds"])
    return papers


def fetch_recent_papers(config: dict[str, Any], cutoff: datetime) -> list[dict[str, Any]]:
    all_papers: list[dict[str, Any]] = []
    successful = 0
    for index, (name, query) in enumerate(config["query_families"].items()):
        LOGGER.info("Processing query family: %s", name)
        try:
            papers = fetch_query_family(name, query, cutoff, config["scraper"])
            successful += 1
            all_papers.extend(papers)
            LOGGER.info("Retrieved %d recent papers for %s", len(papers), name)
        except ArxivRetrievalError as error:
            LOGGER.error("Query family %s failed: %s", name, error)
        if index + 1 < len(config["query_families"]):
            time.sleep(config["scraper"]["request_delay_seconds"])
    if not successful:
        raise ArxivRetrievalError("All arXiv query families failed; existing data was left untouched")
    return all_papers
