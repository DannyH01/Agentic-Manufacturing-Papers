"""Generate GitHub-friendly README and category tables from canonical JSON."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from scraper.utils import atomic_write_text, normalize_whitespace


def paper_sort_key(paper: dict[str, Any]) -> tuple[str, str, str]:
    return (paper.get("updated") or paper.get("published") or "", paper.get("published", ""), paper.get("arxiv_id", ""))


def _escape(value: str) -> str:
    return html.escape(normalize_whitespace(value), quote=False).replace("|", "&#124;")


def _code_label(value: str) -> str:
    """Sanitize trusted labels without HTML-encoding ampersands in code spans."""
    return normalize_whitespace(value).replace("`", "'").replace("|", "/")


def _paper_cell(paper: dict[str, Any]) -> str:
    authors = paper.get("authors", [])
    if len(authors) > 3:
        author_text = f"{authors[0]} et al."
    else:
        author_text = ", ".join(authors)
    date = str(paper.get("published", ""))[:10]
    return f"[{_escape(paper['title'])}]({paper['arxiv_url']})<br><br>{_escape(author_text)}<br><br>{date}"


def _comments_cell(paper: dict[str, Any], config: dict[str, Any]) -> str:
    category = config["categories"][paper["primary_category"]]["title"]
    tags = paper.get("ai_tags", []) + paper.get("manufacturing_tags", []) + paper.get("research_tags", [])
    pieces = [" ".join(f"`{_code_label(tag)}`" for tag in [category] + tags[:7])]
    if paper.get("comment"):
        pieces.append(_escape(paper["comment"]))
    if paper.get("journal_ref"):
        pieces.append(f"Journal reference: {_escape(paper['journal_ref'])}")
    if paper.get("doi"):
        doi = _escape(paper["doi"])
        pieces.append(f"DOI: [{doi}](https://doi.org/{doi})")
    links = []
    if paper.get("code_url"):
        links.append(f"[Code]({paper['code_url']})")
    if paper.get("project_url"):
        links.append(f"[Project]({paper['project_url']})")
    if links:
        pieces.append(" · ".join(links))
    return "<br>".join(piece for piece in pieces if piece)


def paper_table(papers: list[dict[str, Any]], config: dict[str, Any]) -> str:
    lines = ["| Paper | Abstract | Comments |", "|---|---|---|"]
    for paper in papers:
        lines.append(f"| {_paper_cell(paper)} | {_escape(paper.get('abstract', ''))} | {_comments_cell(paper, config)} |")
    return "\n".join(lines)


def generate_all(papers: list[dict[str, Any]], state: dict[str, Any], config: dict[str, Any], root: Path) -> None:
    sorted_papers = sorted(papers, key=paper_sort_key, reverse=True)
    category_links = "\n".join(
        f"- [{category['title']}](categories/{category['file']})"
        for category in config["categories"].values()
    )
    latest = sorted_papers[:config["display"]["latest_papers"]]
    readme = f"""# Agentic AI for Manufacturing Papers

An automatically updated collection of research on agentic AI, LLM agents, multi-agent systems, autonomous decision making, tool-using AI systems, and related foundation-model applications for manufacturing.

This repository covers manufacturing copilots, digital twins, robotics, process and production planning, quality, maintenance, knowledge systems, engineering workflows, and related intelligent manufacturing systems. Inclusion and classification use automated keyword retrieval and deterministic relevance scoring, so occasional refinements may be needed.

- Last updated: {state.get('last_successful_run') or 'Not yet run'}
- Total papers: {state.get('total_papers', len(papers))}
- New papers this update: {state.get('new_papers_last_update', 0)}
- Updated papers this update: {state.get('updated_papers_last_update', 0)}

## Categories

{category_links}

## Latest papers

{paper_table(latest, config)}

## Data and methodology

[`data/papers.json`](data/papers.json) is the canonical dataset. The CSV, this README, and all category pages are regenerated from it. Search families combine agentic-AI concepts with manufacturing domains, and every accepted paper must pass deterministic relevance filtering. See [`config.yaml`](config.yaml) for queries, weights, categories, and tags.

## Local usage

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scraper.main --force
```

On Windows PowerShell, activate with `.venv\\Scripts\\activate`. Use `--dry-run` to retrieve and classify without modifying tracked files, and `--verbose` for detailed logs.

## Automated updates

The GitHub Actions workflow runs daily, executes tests, and checks whether a full update is due. The scraper performs that update every three days using an overlapping retrieval window; a manual run can force an update. Generated changes are committed only when tracked files actually change.

## License

MIT — see [LICENSE](LICENSE).
"""
    atomic_write_text(root / "README.md", readme)

    for key, category in config["categories"].items():
        selected = [paper for paper in sorted_papers if paper.get("primary_category") == key]
        page = f"""# {category['title']}

{category['description']}

Total papers: {len(selected)}

[Back to the main collection](../README.md)

{paper_table(selected, config)}
"""
        atomic_write_text(root / "categories" / category["file"], page)
