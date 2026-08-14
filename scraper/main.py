"""Command-line orchestration for the literature tracker."""

from __future__ import annotations

import argparse
import csv
import io
import logging
from datetime import timedelta
from pathlib import Path
from typing import Any

from scraper.classify import classify_paper, extract_tags
from scraper.deduplicate import deduplicate_papers, merge_records
from scraper.fetch_arxiv import ArxivRetrievalError, fetch_recent_papers
from scraper.generate_markdown import generate_all, paper_sort_key
from scraper.relevance import is_relevant
from scraper.utils import ROOT, atomic_write_json, atomic_write_text, isoformat, load_config, load_json, parse_datetime, utc_now

LOGGER = logging.getLogger(__name__)
DATA_FIELDS = [
    "arxiv_id", "version", "title", "authors", "abstract", "published", "updated",
    "arxiv_url", "pdf_url", "arxiv_primary_category", "arxiv_categories", "comment",
    "journal_ref", "doi", "code_url", "project_url", "primary_category", "category_score",
    "relevance_score", "ai_tags", "manufacturing_tags", "research_tags", "matched_keywords",
    "matched_query_families", "first_seen", "last_seen",
]


def default_state() -> dict[str, Any]:
    return {
        "last_successful_run": None,
        "last_full_update": None,
        "total_papers": 0,
        "new_papers_last_update": 0,
        "updated_papers_last_update": 0,
    }


def update_is_due(state: dict[str, Any], interval_days: int, now: Any) -> bool:
    previous = parse_datetime(state.get("last_full_update"))
    return previous is None or now - previous >= timedelta(days=interval_days)


def process_candidates(candidates: list[dict[str, Any]], config: dict[str, Any], seen_at: str) -> tuple[list[dict[str, Any]], int]:
    accepted: list[dict[str, Any]] = []
    rejected = 0
    for paper in deduplicate_papers(candidates):
        relevant, relevance_score, matches = is_relevant(paper, config)
        if not relevant:
            rejected += 1
            continue
        primary, category_score, _ = classify_paper(paper, config)
        paper.update(extract_tags(paper, config))
        paper.update({
            "primary_category": primary,
            "category_score": category_score,
            "relevance_score": relevance_score,
            "matched_keywords": matches,
            "first_seen": seen_at,
            "last_seen": seen_at,
        })
        accepted.append(paper)
        LOGGER.info("Accepted paper (score=%d, category=%s): %s",
                    relevance_score, primary, paper.get("title", paper.get("arxiv_id", "unknown")))
    return accepted, rejected


def revalidate_existing(papers: list[dict[str, Any]], config: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    """Reapply current policy so configuration refinements can remove stale false positives."""
    valid: list[dict[str, Any]] = []
    removed = 0
    for paper in deduplicate_papers(papers):
        relevant, relevance_score, matches = is_relevant(paper, config)
        if not relevant:
            removed += 1
            continue
        primary, category_score, _ = classify_paper(paper, config)
        paper.update(extract_tags(paper, config))
        paper.update({
            "primary_category": primary,
            "category_score": category_score,
            "relevance_score": relevance_score,
            "matched_keywords": matches,
        })
        valid.append(paper)
    return valid, removed


def write_csv(path: Path, papers: list[dict[str, Any]]) -> None:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=DATA_FIELDS, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for paper in papers:
        row = dict(paper)
        for field in ("authors", "arxiv_categories", "ai_tags", "manufacturing_tags", "research_tags",
                      "matched_keywords", "matched_query_families"):
            row[field] = " | ".join(str(value) for value in row.get(field, []))
        writer.writerow(row)
    atomic_write_text(path, buffer.getvalue())


def run(force: bool = False, dry_run: bool = False, root: Path = ROOT) -> int:
    config = load_config(root / "config.yaml")
    state_path = root / "data" / "state.json"
    papers_path = root / "data" / "papers.json"
    state = load_json(state_path, default_state())
    now = utc_now()

    LOGGER.info("Starting paper update")
    LOGGER.info("Last full update: %s", state.get("last_full_update"))
    if not force and not update_is_due(state, config["scraper"]["update_interval_days"], now):
        LOGGER.info("Full update not required yet.")
        return 0

    cutoff = now - timedelta(days=config["scraper"]["lookback_days"])
    existing = load_json(papers_path, [])
    if not isinstance(existing, list):
        raise ValueError("data/papers.json must contain a JSON array")

    candidates = fetch_recent_papers(config, cutoff)
    timestamp = isoformat(now)
    accepted, rejected = process_candidates(candidates, config, timestamp)
    LOGGER.info("Papers retrieved: %d raw, %d unique; accepted: %d; rejected by relevance filter: %d",
                len(candidates), len(accepted) + rejected, len(accepted), rejected)
    existing, removed_count = revalidate_existing(existing, config)
    if removed_count:
        LOGGER.info("Removed %d existing papers that no longer pass relevance policy", removed_count)
    merged, new_count, updated_count = merge_records(existing, accepted)
    merged = sorted(deduplicate_papers(merged), key=paper_sort_key, reverse=True)
    LOGGER.info("New papers added: %d; existing papers updated: %d", new_count, updated_count)

    if dry_run:
        LOGGER.info("Dry run complete: would store %d papers; no files changed", len(merged))
        return 0

    new_state = {
        "last_successful_run": timestamp,
        "last_full_update": timestamp,
        "total_papers": len(merged),
        "new_papers_last_update": new_count,
        "updated_papers_last_update": updated_count,
    }
    atomic_write_json(papers_path, merged)
    write_csv(root / "data" / "papers.csv", merged)
    atomic_write_json(state_path, new_state)
    generate_all(merged, new_state, config, root)
    LOGGER.info("Database saved and Markdown generated")
    LOGGER.info("Update complete")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track Agentic AI for Manufacturing papers on arXiv")
    parser.add_argument("--force", action="store_true", help="bypass the three-day update interval")
    parser.add_argument("--dry-run", action="store_true", help="retrieve and classify without writing files")
    parser.add_argument("--verbose", action="store_true", help="enable debug logging")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        return run(force=args.force, dry_run=args.dry_run)
    except ArxivRetrievalError as error:
        LOGGER.error("Update aborted safely: %s", error)
        return 1
    except Exception:
        LOGGER.exception("Update failed; existing canonical data was preserved where possible")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
