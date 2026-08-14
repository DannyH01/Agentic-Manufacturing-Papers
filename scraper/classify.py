"""Primary-category and secondary-tag assignment."""

from __future__ import annotations

from typing import Any

from scraper.utils import matching_phrases


def classify_paper(paper: dict[str, Any], config: dict[str, Any]) -> tuple[str, int, dict[str, int]]:
    weights = config["category_field_weights"]
    scores: dict[str, int] = {}
    for key, category in config["categories"].items():
        phrases = category["keywords"]
        score = 0
        for field in ("title", "abstract", "comment"):
            score += len(matching_phrases(paper.get(field, ""), phrases)) * weights[field]
        scores[key] = score

    priority = {key: index for index, key in enumerate(config["category_priority"])}
    primary = min(scores, key=lambda key: (-scores[key], priority.get(key, len(priority)), key))
    return primary, scores[primary], scores


def extract_tags(paper: dict[str, Any], config: dict[str, Any]) -> dict[str, list[str]]:
    text = " ".join((paper.get("title", ""), paper.get("abstract", ""), paper.get("comment", "")))
    result: dict[str, list[str]] = {}
    for group in ("ai", "manufacturing", "research"):
        result[f"{group}_tags"] = [
            tag for tag, phrases in config["tags"][group].items() if matching_phrases(text, phrases)
        ]
    return result
