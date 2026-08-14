import pytest

from scraper.classify import classify_paper
from scraper.utils import load_config


CONFIG = load_config()


@pytest.mark.parametrize(
    ("title", "abstract", "expected"),
    [
        ("An LLM Agent for Job-Shop Scheduling", "Production scheduling in a smart factory.", "production_planning_scheduling"),
        ("Multi-Agent CNC Process Planning", "Operation planning for machining.", "process_planning"),
        ("An LLM Predictive Maintenance System", "Fault diagnosis and condition monitoring for machines.", "monitoring_diagnostics_maintenance"),
        ("An Agentic Digital Twin for Manufacturing", "A virtual manufacturing simulation.", "digital_twins_simulation"),
    ],
)
def test_representative_category_assignments(title, abstract, expected):
    primary, score, _ = classify_paper({"title": title, "abstract": abstract, "comment": ""}, CONFIG)
    assert primary == expected
    assert score > 0


def test_classification_always_has_exactly_one_primary_category():
    primary, score, scores = classify_paper({"title": "Agentic Manufacturing", "abstract": "", "comment": ""}, CONFIG)
    assert primary in CONFIG["categories"]
    assert isinstance(score, int)
    assert len(scores) == len(CONFIG["categories"])
