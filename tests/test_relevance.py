from scraper.relevance import is_relevant, score_relevance
from scraper.utils import load_config


CONFIG = load_config()


def paper(title: str, abstract: str) -> dict[str, str]:
    return {"title": title, "abstract": abstract, "comment": ""}


def test_relevant_agentic_manufacturing_paper_is_accepted():
    accepted, score, matches = is_relevant(
        paper("An LLM Agent for Smart Manufacturing", "The system performs autonomous process planning for CNC machining."),
        CONFIG,
    )
    assert accepted
    assert score >= CONFIG["relevance"]["minimum_score"]
    assert "LLM agent" in [match.casefold() == "llm agent" and match or "" for match in matches]


def test_generic_manufacturing_paper_without_agentic_ai_is_rejected():
    accepted, _, _ = is_relevant(
        paper("Thermal Modeling for Additive Manufacturing", "A finite element model predicts residual stress."), CONFIG
    )
    assert not accepted


def test_generic_agent_paper_without_manufacturing_is_rejected():
    accepted, _, _ = is_relevant(
        paper("Autonomous Agents for Online Shopping", "A tool-using agent selects consumer products."), CONFIG
    )
    assert not accepted


def test_nonmanufacturing_production_context_is_rejected():
    accepted, _, _ = is_relevant(
        paper(
            "Agentic AI for Indie Game Production Planning",
            "The platform coordinates video game developers and generates a production plan.",
        ),
        CONFIG,
    )
    assert not accepted


def test_ambiguous_process_control_phrase_is_rejected_without_domain_anchor():
    accepted, _, _ = is_relevant(
        paper("Memory for AI Agents", "The runtime adds an in-process control-plane for reliable writes."), CONFIG
    )
    assert not accepted


def test_automated_experimentation_without_agentic_ai_is_rejected():
    accepted, _, _ = is_relevant(
        paper(
            "An Automated Magnetron Sputtering Chamber",
            "Manufacturing processes are accelerated by automated and autonomous experimentation. "
            "The instrumentation performs synchronized data collection and system control.",
        ),
        CONFIG,
    )
    assert not accepted


def test_title_matches_are_weighted_more_than_abstract_only_matches():
    title_score, _ = score_relevance(
        paper("LLM Agent for Manufacturing", "We present a benchmark."), CONFIG
    )
    abstract_score, _ = score_relevance(
        paper("A New Benchmark", "We study an LLM agent for manufacturing."), CONFIG
    )
    assert title_score > abstract_score
