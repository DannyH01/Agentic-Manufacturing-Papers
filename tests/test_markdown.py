from scraper.generate_markdown import paper_table
from scraper.utils import load_config


def test_category_ampersand_is_not_rendered_as_html_entity():
    config = load_config()
    paper = {
        "title": "Inspection Agent",
        "authors": ["A. Author"],
        "abstract": "An abstract.",
        "published": "2026-01-01T00:00:00Z",
        "arxiv_url": "https://arxiv.org/abs/2601.00001",
        "primary_category": "quality_inspection_metrology",
        "ai_tags": [],
        "manufacturing_tags": [],
        "research_tags": [],
    }
    table = paper_table([paper], config)
    assert "`Quality, Inspection & Metrology`" in table
    assert "Inspection &amp; Metrology" not in table


def test_full_abstract_is_collapsed_in_details_element():
    config = load_config()
    abstract = "This is the complete original abstract, including all of its text."
    paper = {
        "title": "Manufacturing Agent",
        "authors": ["A. Author"],
        "abstract": abstract,
        "published": "2026-01-01T00:00:00Z",
        "arxiv_url": "https://arxiv.org/abs/2601.00002",
        "primary_category": "agentic_frameworks",
        "ai_tags": [],
        "manufacturing_tags": [],
        "research_tags": [],
    }
    table = paper_table([paper], config)
    assert f"<details><summary>Show abstract</summary><br>{abstract}</details>" in table
    assert "<details open>" not in table
