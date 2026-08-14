# Agentic AI for Manufacturing Papers

An automatically updated collection of research on agentic AI, LLM agents, multi-agent systems, autonomous decision making, tool-using AI systems, and related foundation-model applications for manufacturing.

This repository covers manufacturing copilots, digital twins, robotics, process and production planning, quality, maintenance, knowledge systems, engineering workflows, and related intelligent manufacturing systems. Inclusion and classification use automated keyword retrieval and deterministic relevance scoring, so occasional refinements may be needed.

- Last updated: 2026-08-14T18:10:20Z
- Total papers: 0
- New papers this update: 0
- Updated papers this update: 0

## Categories

- [Agentic Manufacturing Frameworks](categories/agentic-frameworks.md)
- [Process Planning & Decision Making](categories/process-planning.md)
- [Process Optimization & Control](categories/process-optimization-control.md)
- [Production Planning & Scheduling](categories/production-planning-scheduling.md)
- [Monitoring, Diagnostics & Maintenance](categories/monitoring-diagnostics-maintenance.md)
- [Quality, Inspection & Metrology](categories/quality-inspection-metrology.md)
- [Robotics & Autonomous Manufacturing](categories/robotics-autonomous-manufacturing.md)
- [Digital Twins & Simulation](categories/digital-twins-simulation.md)
- [Knowledge & Manufacturing Intelligence](categories/knowledge-manufacturing-intelligence.md)
- [Human-AI Collaboration](categories/human-ai-collaboration.md)
- [Design & Manufacturing Engineering](categories/design-manufacturing-engineering.md)
- [Scientific Discovery & Experimentation](categories/scientific-discovery.md)

## Latest papers

| Paper | Abstract | Comments |
|---|---|---|

## Data and methodology

[`data/papers.json`](data/papers.json) is the canonical dataset. The CSV, this README, and all category pages are regenerated from it. Search families combine agentic-AI concepts with manufacturing domains, and every accepted paper must pass deterministic relevance filtering. See [`config.yaml`](config.yaml) for queries, weights, categories, and tags.

## Local usage

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scraper.main --force
```

On Windows PowerShell, activate with `.venv\Scripts\activate`. Use `--dry-run` to retrieve and classify without modifying tracked files, and `--verbose` for detailed logs.

## Automated updates

The GitHub Actions workflow runs daily, executes tests, and checks whether a full update is due. The scraper performs that update every three days using an overlapping retrieval window; a manual run can force an update. Generated changes are committed only when tracked files actually change.

## License

MIT — see [LICENSE](LICENSE).
