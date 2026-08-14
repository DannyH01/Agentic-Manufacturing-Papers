"""arXiv identifier normalization and deterministic record merging."""

from __future__ import annotations

import re
from typing import Any, Iterable

VERSION_RE = re.compile(r"v(\d+)$", re.IGNORECASE)


def base_arxiv_id(identifier: str) -> str:
    identifier = identifier.strip().rstrip("/")
    if "/abs/" in identifier:
        identifier = identifier.split("/abs/", 1)[1]
    elif "/pdf/" in identifier:
        identifier = identifier.split("/pdf/", 1)[1]
    identifier = re.sub(r"\.pdf$", "", identifier, flags=re.IGNORECASE)
    return VERSION_RE.sub("", identifier)


def version_number(value: str | int | None) -> int:
    if isinstance(value, int):
        return value
    match = VERSION_RE.search(str(value or ""))
    if match:
        return int(match.group(1))
    try:
        return int(value or 1)
    except ValueError:
        return 1


def deduplicate_papers(papers: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for paper in papers:
        original_id = str(paper.get("arxiv_id", ""))
        base_id = base_arxiv_id(original_id)
        if not base_id:
            continue
        candidate = dict(paper)
        candidate["arxiv_id"] = base_id
        if not candidate.get("version"):
            match = VERSION_RE.search(original_id)
            candidate["version"] = f"v{match.group(1)}" if match else "v1"
        current = records.get(base_id)
        if current is None or version_number(candidate.get("version")) > version_number(current.get("version")):
            if current:
                candidate["first_seen"] = current.get("first_seen", candidate.get("first_seen", ""))
                candidate["matched_query_families"] = sorted(set(
                    current.get("matched_query_families", []) + candidate.get("matched_query_families", [])
                ))
            records[base_id] = candidate
        elif version_number(candidate.get("version")) == version_number(current.get("version")):
            current["matched_query_families"] = sorted(set(
                current.get("matched_query_families", []) + candidate.get("matched_query_families", [])
            ))
    return list(records.values())


def merge_records(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int, int]:
    merged = {base_arxiv_id(p["arxiv_id"]): dict(p) for p in deduplicate_papers(existing)}
    new_count = updated_count = 0
    for paper in deduplicate_papers(incoming):
        key = paper["arxiv_id"]
        old = merged.get(key)
        if old is None:
            merged[key] = paper
            new_count += 1
        elif version_number(paper.get("version")) > version_number(old.get("version")):
            paper["first_seen"] = old.get("first_seen", paper.get("first_seen", ""))
            merged[key] = paper
            updated_count += 1
        elif version_number(paper.get("version")) == version_number(old.get("version")):
            # Refresh metadata without counting an unchanged version as a revision.
            paper["first_seen"] = old.get("first_seen", paper.get("first_seen", ""))
            merged[key] = paper
    return list(merged.values()), new_count, updated_count
