"""Deterministic relevance scoring for agentic manufacturing research."""

from __future__ import annotations

from typing import Any

from scraper.utils import matching_phrases


def _field_agentic_matches(text: str, keywords: dict[str, Any]) -> list[str]:
    """Return explicit and contextually agentic evidence within one metadata field."""
    matches = matching_phrases(text, keywords["agentic"])
    models = matching_phrases(text, keywords.get("ai_models", []))
    capabilities = matching_phrases(text, keywords.get("agentic_capabilities", []))
    generic_agents = matching_phrases(text, keywords.get("generic_agents", []))
    manufacturing_context = matching_phrases(text, keywords.get("manufacturing_context", []))
    if models and capabilities:
        matches.extend(models + capabilities)
    if generic_agents and manufacturing_context:
        matches.extend(generic_agents)
    return sorted(set(matches), key=str.casefold)


def score_relevance(paper: dict[str, Any], config: dict[str, Any]) -> tuple[int, list[str]]:
    rules = config["relevance"]
    keywords = config["keywords"]
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")
    comment = paper.get("comment", "")

    title_agentic = _field_agentic_matches(title, keywords)
    title_manufacturing = matching_phrases(title, keywords["manufacturing"])
    abstract_agentic = _field_agentic_matches(abstract, keywords)
    abstract_manufacturing = matching_phrases(abstract, keywords["manufacturing"])
    comment_agentic = _field_agentic_matches(comment, keywords)
    comment_manufacturing = matching_phrases(comment, keywords["manufacturing"])

    has_agentic = bool(title_agentic or abstract_agentic or comment_agentic)
    has_manufacturing = bool(title_manufacturing or abstract_manufacturing or comment_manufacturing)
    score = 0
    score += rules["title_agentic_weight"] if title_agentic else 0
    score += rules["title_manufacturing_weight"] if title_manufacturing else 0
    score += rules["abstract_agentic_weight"] if abstract_agentic else 0
    score += rules["abstract_manufacturing_weight"] if abstract_manufacturing else 0
    score += rules["comments_agentic_weight"] if comment_agentic else 0
    score += rules["comments_manufacturing_weight"] if comment_manufacturing else 0
    score += rules["combined_domain_weight"] if has_agentic and has_manufacturing else 0

    application_matches = matching_phrases(" ".join((title, abstract, comment)), keywords["applications"])
    score += rules["application_weight"] if application_matches else 0

    matches = sorted(
        set(title_agentic + title_manufacturing + abstract_agentic + abstract_manufacturing +
            comment_agentic + comment_manufacturing + application_matches),
        key=str.casefold,
    )
    return score, matches


def is_relevant(paper: dict[str, Any], config: dict[str, Any]) -> tuple[bool, int, list[str]]:
    score, matches = score_relevance(paper, config)
    combined = " ".join((paper.get("title", ""), paper.get("abstract", ""), paper.get("comment", "")))
    agentic = matching_phrases(combined, config["keywords"]["agentic"])
    agentic_core = matching_phrases(combined, config["keywords"]["agentic_core"])
    models = matching_phrases(combined, config["keywords"].get("ai_models", []))
    capabilities = matching_phrases(combined, config["keywords"].get("agentic_capabilities", []))
    generic_agents = matching_phrases(combined, config["keywords"].get("generic_agents", []))
    manufacturing = matching_phrases(combined, config["keywords"]["manufacturing"])
    manufacturing_context = matching_phrases(combined, config["keywords"]["manufacturing_context"])
    exclusions = matching_phrases(combined, config["keywords"].get("exclusions", []))

    # Both sides of the scope are mandatory. Excluded senses only veto a paper
    # when no explicit, stronger agentic phrase beyond the excluded phrase exists.
    explicit_agentic = bool(agentic_core)
    model_with_capability = bool(models and capabilities)
    contextual_agent = bool(generic_agents and manufacturing_context)
    accepted = bool((explicit_agentic or model_with_capability or contextual_agent) and
                    manufacturing and manufacturing_context and
                    score >= config["relevance"]["minimum_score"])
    if exclusions and not (explicit_agentic or model_with_capability):
        accepted = False
    return accepted, score, matches
