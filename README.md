# Agentic AI for Manufacturing Papers

An automatically updated collection of research on agentic AI, LLM agents, multi-agent systems, autonomous decision making, tool-using AI systems, and related foundation-model applications for manufacturing.

This repository covers manufacturing copilots, digital twins, robotics, process and production planning, quality, maintenance, knowledge systems, engineering workflows, and related intelligent manufacturing systems. Inclusion and classification use automated keyword retrieval and deterministic relevance scoring, so occasional refinements may be needed.

- Last updated: 2026-08-14T18:41:04Z
- Total papers: 4
- New papers this update: 4
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
| [Memory-Augmented Reinforcement Learning Agent for CAD Generation](https://arxiv.org/abs/2605.19748v2)<br><br>Yin Xiaolong et al.<br><br>2026-05-19 | Automatic generation of computer-aided design (CAD) models is a core technology for enabling intelligence in advanced manufacturing. Existing generation methods based on large language models (LLMs) often fall short when handling complex CAD models characterized by long operation sequences, diverse operation types, and strong geometric constraints, primarily because reasoning chains break and effective error-correction mechanisms are lacking. To address this problem, this paper proposes a memory-augmented reinforcement learning framework for CAD generation agents. The framework encapsulates the underlying geometric kernel into a structured toolchain callable by the agent and builds a closed-loop mechanism of design intent understanding, global planning, execution, and multi-dimensional verification. It also designs a dual-track memory module consisting of a case library and a skill library, and proposes a dynamic utility retrieval algorithm. By introducing reinforcement learning into retrieval and policy optimization, the agent can effectively avoid retrieval traps in which examples are semantically similar but geometrically infeasible, enabling online self-correction and continual evolution without additional large-scale annotated data. Experiments show that the proposed method significantly improves both the success rate and geometric consistency on complex CAD model generation tasks. | `Design &amp; Manufacturing Engineering` `memory` `reinforcement-learning` `manufacturing` `CAD` `optimization` `planning`<br>We are withdrawing this manuscript because we have identified issues in the current analysis that require substantial revision. Until these issues are resolved, we do not consider the present version suitable for citation |
| [Direct Laser Interference Patterning of Functional Metal Surfaces: From Written Geometry to Functional Interfaces](https://arxiv.org/abs/2608.09545v1)<br><br>Petr Hauschwitz<br><br>2026-08-10 | Direct laser interference patterning (DLIP) generates periodic micro- and nanoscale structures with increasing precision and throughput, yet similar geometries can produce fundamentally different functional responses. This review examines why morphology alone cannot predict friction, wetting and ice adhesion, bacterial response, cell behaviour, optical performance or electrochemical and photovoltaic function. DLIP is treated as a model system in which the optically prescribed geometry can be distinguished from the interface realised during processing. The written period is separated from relief depth, aspect ratio, hierarchical topography, surface chemistry, ageing and process history. Functional response is interpreted as a two-stage process: geometry creates the opportunity for interaction with an external agent, while the realised interface determines how that interaction becomes measurable performance under a specific interfacial state. A curated, metals-centred evidence base spanning tribology, wetting and anti-icing, antibacterial and biomedical surfaces, optics, electrochemistry, energy devices and manufacturing shows that period-depth coordinates alone rarely predict function across domains. Geometry remains highly transferable in optical systems and controlled mechanical contacts, whereas biological, state-dependent and device-level functions also depend on surface state, operating conditions and system architecture. The framework reconciles conflicting observations and identifies which variables are transferable and which remain context-dependent. Predictive DLIP surface engineering therefore requires identification of the interacting agent, separation of written geometry from the realised interface, isolation of variables governing interfacial coupling and evaluation through direct, mechanism-specific endpoints. | `Production Planning &amp; Scheduling` `manufacturing`<br>Review article, 6 figures, 2 tables |
| [ConMem: Contribution-Aware Memory for Long-Horizon Manufacturing Inspection Logs](https://arxiv.org/abs/2607.28126v2)<br><br>Bingchen Liu et al.<br><br>2026-07-30 | Long-horizon steel-equipment inspection requires reasoning over heterogeneous records accumulated across repeated inspection cycles. Existing retrieval-augmented generation systems treat historical logs as a static corpus and retain records without estimating their diagnostic value, failing to report early risk. To this end, we propose ConMem, a contribution-aware memory framework for LLM-assisted equipment inspection, supporting a human-in-the-loop early-risk screening system. Specifically, our ConMem first segments inspection logs into functional evidence units, then estimates each memory unit's contribution to downstream diagnosis through a Shapley-style estimation, and finally retains high-value evidence under a constrained memory budget. In experiments, we evaluate ConMem on real-world dataset and ConMem achieves 76.0% QA accuracy, exceeding the strongest directly comparable baseline. Relative to the naive 8K-context LLM baselines, it reduces the average number of input tokens by 88.2% and response time by 86.6%. Ablation studies also show that the functional-role-aware segmentation and contribution-based valuation are helping prioritize weak degradation signals for targeted field inspection. Practical deployments further confirm that ConMem retains the weak early signal across three inspection cycles, providing an early-stage seal-wear alert targeted for on-site inspectors. | `Quality, Inspection &amp; Metrology` `LLM` `RAG` `human-in-the-loop` `manufacturing` `inspection` `human-AI-collaboration` |
| [SHRIMP: Iterative Refinement of Robot Task Plans](https://arxiv.org/abs/2608.08884v1)<br><br>Mya Schroder et al.<br><br>2026-08-09 | As collaborative robots have entered domains such as manufacturing, agriculture, and healthcare, programming or adapting robot behavior typically requires robotic expertise that most end users lack. Natural language lowers this barrier. Recent advancements in large language models (LLMs) have made it feasible to translate natural language into robot task plans. However, language-based task specification suffers from semantic ambiguity, and generative models lack transparency for how language instructions become robot actions, making it difficult for users to validate the plan before execution. To address these issues, we introduce SHRIMP, a system that allows users to automatically generate a hierarchical robot primitive plan using natural language and iteratively revise their plan through re-prompting and explicit correction. At each revision, SHRIMP allows users to validate their plan in simulation, and once satisfied, execute it on the physical robot. Through a user study involving participants planning tabletop kitchen tasks (n=35), we validate that SHRIMP improves perceived control and enhances robot transparency. System videos and source code are available at https://wisc-hci.github.io/SHRIMP. | `Production Planning &amp; Scheduling` `simulation` `manufacturing` `robotics` `planning`<br>11 pages, 8 figures, The 39th Annual ACM Symposium on User Interface Software and Technology (UIST '26)<br>DOI: [10.1145/3830398.3830644](https://doi.org/10.1145/3830398.3830644)<br>[Project](https://wisc-hci.github.io/SHRIMP) |

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
