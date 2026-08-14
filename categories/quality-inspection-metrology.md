# Quality, Inspection & Metrology

Agentic quality assurance, inspection, defect analysis, and metrology.

Total papers: 1

[Back to the main collection](../README.md)

| Paper | Abstract | Comments |
|---|---|---|
| [ConMem: Contribution-Aware Memory for Long-Horizon Manufacturing Inspection Logs](https://arxiv.org/abs/2607.28126v2)<br><br>Bingchen Liu et al.<br><br>2026-07-30 | <details><summary>Show abstract</summary><br>Long-horizon steel-equipment inspection requires reasoning over heterogeneous records accumulated across repeated inspection cycles. Existing retrieval-augmented generation systems treat historical logs as a static corpus and retain records without estimating their diagnostic value, failing to report early risk. To this end, we propose ConMem, a contribution-aware memory framework for LLM-assisted equipment inspection, supporting a human-in-the-loop early-risk screening system. Specifically, our ConMem first segments inspection logs into functional evidence units, then estimates each memory unit's contribution to downstream diagnosis through a Shapley-style estimation, and finally retains high-value evidence under a constrained memory budget. In experiments, we evaluate ConMem on real-world dataset and ConMem achieves 76.0% QA accuracy, exceeding the strongest directly comparable baseline. Relative to the naive 8K-context LLM baselines, it reduces the average number of input tokens by 88.2% and response time by 86.6%. Ablation studies also show that the functional-role-aware segmentation and contribution-based valuation are helping prioritize weak degradation signals for targeted field inspection. Practical deployments further confirm that ConMem retains the weak early signal across three inspection cycles, providing an early-stage seal-wear alert targeted for on-site inspectors.</details> | `Quality, Inspection & Metrology` `LLM` `RAG` `human-in-the-loop` `manufacturing` `inspection` `human-AI-collaboration` |
