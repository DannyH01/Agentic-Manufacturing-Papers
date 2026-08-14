"""Conversion of Atom entries into stable paper records and URL metadata."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from scraper.deduplicate import base_arxiv_id
from scraper.utils import normalize_whitespace

URL_RE = re.compile(r"https?://[^\s<>\])}\"']+", re.IGNORECASE)
CODE_HOSTS = {"github.com", "www.github.com", "gitlab.com", "www.gitlab.com", "codeberg.org", "www.codeberg.org"}


def extract_urls(*values: str) -> tuple[str, str]:
    code_url = project_url = ""
    for value in values:
        for raw_url in URL_RE.findall(value or ""):
            url = raw_url.rstrip(".,;:")
            host = urlparse(url).netloc.casefold()
            if host in CODE_HOSTS and not code_url:
                code_url = url
            elif host and host not in {"arxiv.org", "doi.org", "dx.doi.org"} and not project_url:
                project_url = url
    return code_url, project_url


def _entry_value(entry: Any, key: str, default: Any = "") -> Any:
    if isinstance(entry, dict):
        return entry.get(key, default)
    return getattr(entry, key, default)


def entry_to_paper(entry: Any) -> dict[str, Any]:
    entry_id = str(_entry_value(entry, "id"))
    base_id = base_arxiv_id(entry_id)
    version_match = re.search(r"v(\d+)$", entry_id.rstrip("/"), flags=re.IGNORECASE)
    version = f"v{version_match.group(1)}" if version_match else "v1"

    links = _entry_value(entry, "links", []) or []
    arxiv_url = f"https://arxiv.org/abs/{base_id}"
    pdf_url = f"https://arxiv.org/pdf/{base_id}"
    for link in links:
        href = str(_entry_value(link, "href"))
        if _entry_value(link, "rel") == "alternate":
            arxiv_url = href
        if _entry_value(link, "type") == "application/pdf" or _entry_value(link, "title") == "pdf":
            pdf_url = href

    comment = normalize_whitespace(_entry_value(entry, "arxiv_comment"))
    journal_ref = normalize_whitespace(_entry_value(entry, "arxiv_journal_ref"))
    doi = normalize_whitespace(_entry_value(entry, "arxiv_doi"))
    abstract = normalize_whitespace(_entry_value(entry, "summary"))
    code_url, project_url = extract_urls(comment, journal_ref, abstract)
    tags = _entry_value(entry, "tags", []) or []
    categories = [str(_entry_value(tag, "term")) for tag in tags if _entry_value(tag, "term")]
    primary = _entry_value(_entry_value(entry, "arxiv_primary_category", {}), "term")
    authors = [normalize_whitespace(_entry_value(author, "name")) for author in (_entry_value(entry, "authors", []) or [])]

    return {
        "arxiv_id": base_id,
        "version": version,
        "title": normalize_whitespace(_entry_value(entry, "title")),
        "authors": authors,
        "abstract": abstract,
        "published": str(_entry_value(entry, "published")),
        "updated": str(_entry_value(entry, "updated")),
        "arxiv_url": arxiv_url,
        "pdf_url": pdf_url,
        "arxiv_primary_category": str(primary or (categories[0] if categories else "")),
        "arxiv_categories": categories,
        "comment": comment,
        "journal_ref": journal_ref,
        "doi": doi,
        "code_url": code_url,
        "project_url": project_url,
    }
