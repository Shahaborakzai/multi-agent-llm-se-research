![Status](https://img.shields.io/badge/Status-Active-success)
![Institution](https://img.shields.io/badge/Institution-ITMO_University-blue)
![Framework](https://img.shields.io/badge/Framework-OpenHands_CodeAct-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Model](https://img.shields.io/badge/Model-claude--haiku--4--5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Multi-Agent LLM Evaluation for Software Engineering

**ITMO University | Faculty of Artificial Intelligence Technologies (FATII)**
**Student:** Shahab Ali | ID: 503271 | Group: J4132
**Supervisor:** Professor Sergey Kovalchuk | 2025–2026

---

## Key Findings

| Finding | Result |
|---|---|
| Role identity alone ("You are a Coder") | 0/20 — zero effect |
| Output format constraint added | 20/20 — the critical component |
| Adding a Tester (SWE-bench) | 20/30 vs 22/30 baseline — net-negative, 99 s slower |
| Learned role selector | 94.5% vs 95.1% trivial policy — does not beat it |
| Where configuration matters | 19 of 164 tasks (8 rescued, 11 lost) |

**Total: 937 runs · one model · one variable**

---

## Project Overview

This research evaluates how different multi-agent role configurations affect LLM agent performance on standard software engineering benchmarks. The same underlying model is tested across four role configurations to isolate the effect of role assignment from model capability.

**Total experimental runs: 937**

| Component | Count |
|---|---|
| HumanEval (164 tasks × 4 configurations) | 656 runs |
| SWE-bench Lite (30 tasks × 4 configurations) | 120 runs |
| Prompt ablation (20 tasks × 7 variants) | 140 runs |
| Phase 1 (early experiments) | 21 runs |
| **Phase 2 total** | **916** |
| **All-time total** | **937** |

---

## Research Questions

| RQ | Question | Answer |
|---|---|---|
| RQ1 | Which agent roles exist in LLM-based SE frameworks? | 7-layer taxonomy from 19 sources |
| RQ2 | Which prompt component produces the effect? | The output constraint, not the persona |
| RQ3 | Can configuration be predicted from the task? | No — ceiling effect, negative result |

---

## Semester 1 — Structured Literature Review (RQ1)

Following PRISMA-style inclusion criteria, 19 sources were analysed (2023–2025): 7 multi-agent systems and 12 surveys, taxonomies and empirical studies.

**Search Keywords:** ("Large Language Model" OR "LLM") AND ("Software Engineering") AND ("Multi-agent" OR "Role-based")

**7-layer Agent Role Taxonomy:**

    Agent Roles — 7 Layers
    ├── 1. Orchestration      → Manager, Supervisor, Project Coordinator (5 sources)
    ├── 2. Analysis/Planning  → Planner, Requirement Analyst (5 sources)
    ├── 3. Design             → Architect, System Modeler (4 sources)
    ├── 4. Implementation     → Coder, Executor (5 sources)
    ├── 5. Quality Assurance  → Tester, Reviewer, Debugger (5 of 7 systems — largest)
    ├── 6. Knowledge          → KG Curator, Documentation Writer (8 sources)
    └── 7. Operations         → Tooling, Environment Interface (6 sources)

**Key Frameworks:**

| Framework | Year | Core Roles | Key Technique |
|---|---|---|---|
| MetaGPT | 2024 | PM, Architect, Engineer, QA | SOPs to guide workflows |
| ChatDev | 2024 | CEO, CTO, Programmer, Reviewer | Waterfall + Chat Chain |
| Magentic-One | 2025 | Manager, Specialist Agents | Manager-Worker orchestration |
| PotPie | 2025 | Debugger, Tester, KG Curator | Knowledge Graph grounding |

**Key Trend:** Shift from code generation to verification — the QA layer dominates (5 of the 7 systems; 9 of 19 sources).

---

## Semester 2 — Initial Experiments (Phase 1)

Tested local vs cloud LLMs within OpenHands CodeAct framework. 21 runs total.

**HumanEval (15 tasks):**

| Config | LLM | Pass% |
|---|---|---|
| Single Coder | Local 7B | 0% |
| Coder+Tester | Local 7B | 0% |
| Single Coder | Cloud 120B | 100% |
| Coder+Tester | Cloud 120B | 100% |

> Note: the 7B condition covers two HumanEval tasks plus deployment attempts — an infrastructure finding, not a benchmark result.

**SWE-bench (6 tasks, different tasks before/after):**

| Condition | Pass Rate |
|---|---|
| Without Anti-Paralysis instruction | 33.3% |
| With Anti-Paralysis instruction | 100% |

> An observation on six different tasks that motivated the redesign, not a controlled comparison.

**Key Discoveries:**

**1. Self-Healing Phenomenon** — 120B model autonomously recovered from errors in 9/10 cases (90% recovery rate).

**2. Agentic Paralysis** — a failure mode where agents reason correctly but fail to execute the tool call.

**3. Ten Failure Types** catalogued across the runs (XML schema errors, context collapse, verbose paralysis, and 7 more).

---

## Phase 2 — Extended Experiments (2026)

After the first defence identified insufficient sample size, experiments were expanded with a fully automated pipeline.

| Component | Details |
|---|---|
| Framework | OpenHands CodeAct (Docker) |
| Model | claude-haiku-4-5 (same for ALL configurations) |
| HumanEval | 164 tasks (full benchmark) |
| SWE-bench Lite | the first 30 tasks |
| Ablation | the first 20 tasks × 7 prompt variants |
| Timeout | 400 s (HumanEval) · 600 s (SWE-bench) |
| Total Runs | 776 evaluation + 140 ablation = 916 |

**Four Role Configurations:** Baseline (no roles) · Coder only · Coder+Tester · Manager+Coder+Tester

---

### HumanEval Results (pass@1)

| Configuration | Tasks | Pass | Fail | pass@1 | vs Baseline |
|---|---|---|---|---|---|
| Baseline (No Roles) | 164 | 151 | 13 | 92.1% | — |
| Coder Only | 164 | 155 | 9 | 94.5% | +2.4 pp |
| Coder + Tester | 164 | 152 | 12 | 92.7% | +0.6 pp |
| Manager+Coder+Tester | 164 | 156 | 8 | 95.1% | +3.0 pp |

Baseline is the only configuration producing SyntaxErrors (four); every role prompt produced zero.

---

### SWE-bench Lite Results (resolve rate)

| Configuration | Resolved | Failed | Rate | Avg Time | Resolved Avg |
|---|---|---|---|---|---|
| Baseline | 22 | 8 | 73.3% | 296s | 169s |
| **Coder Only** | **25** | **5** | **83.3%** | **232s** | **152s** |
| Coder + Tester | 20 | 10 | 66.7% | 331s | 174s |
| Manager+Coder+Tester | 24 | 6 | 80.0% | 295s | 206s |

> All failures are timeouts, not logic errors. On 30 paired tasks, no pairwise McNemar test can reach significance (minimum achievable p = 0.0625) — the resolve-rate differences are within noise; the timing is the signal.

---

### RQ2 — Prompt Ablation (The Constrained Action Space)

7 prompt variants tested on the first 20 HumanEval tasks (140 runs):

| Variant | Components | pass@1 |
|---|---|---|
| Baseline | No role (constraint only) | 95.0% |
| Coder A | Identity only | 0.0% |
| Coder B | Identity + Responsibility | 0.0% |
| **Coder C** | **Identity + Resp. + Format** | **100.0%** |
| Full A | All titles only | 0.0% |
| Full B | All titles + responsibilities | 0.0% |
| Full C | All full prompts with format | 95.0% |

**Finding:** the output format constraint is the single critical component. Prompt length is ruled out: the constraint-only variant is a short prompt and passes 19/20, while the longest no-constraint variant passes 0/20.

---

### RQ3 — State Prediction (Negative Result)

| Method | pass@1 | Type |
|---|---|---|
| Baseline | 92.1% | Fixed |
| Coder Only | 94.5% | Fixed |
| Coder + Tester | 92.7% | Fixed |
| Manager+Coder+Tester | 95.1% | Fixed |
| **Majority-class policy** | **95.1%** | **Trivial** |
| **State Predictor (DT)** | **94.5%** | **Dynamic** |

The learned selector does **not** beat the trivial always-baseline policy. Ceiling effect: baseline passes 151/164 tasks; only 8 are rescuable by any role (all 8 by the single Coder); 5 are solved by nothing. Role configuration changes the outcome on 19 of 164 tasks; on the remaining 145, all four configurations produce identical results.

**Feature importance (6 of 12 used, rest = 0):** type_count 0.267 · num_words 0.217 · examples 0.159 · uses_list 0.154 · num_lines 0.153 · complex_words 0.050

---

## Repository Structure

    /experiments
      run_eval_v2.py               - HumanEval evaluation script
      swe_eval_proper.py           - SWE-bench evaluation script
      ablation_study.py            - Prompt ablation script (RQ2)
      eval_results.jsonl           - HumanEval raw results (656 runs)
      swe_results_FINAL.jsonl      - SWE-bench raw results (120 runs)
      ablation_results_FINAL.jsonl - Ablation raw results (140 runs)
      q2_state_prediction.txt      - State prediction results (RQ3)
      q2_complete_analysis.txt     - Decision tree rules (RQ3)
    /analysis
      mcnemar_tests.py             - Pairwise McNemar tests
      rq3_baseline.py              - Majority baseline vs decision tree
      decisive_tasks.py            - The 19 disagreeing tasks
    /taxonomy                      - Semester 1 SLR and taxonomy (RQ1)
    /docs                          - Final paper and defence presentation
    /reports                       - Weekly progress reports
    LICENSE                        - MIT

---

## Replication

    # 1. Start OpenHands
    docker run -d --name openhands-eval --memory="4g" \
        -e SANDBOX_VOLUMES="$(pwd)/workspace:/workspace:rw" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -p 3000:3000 \
        ghcr.io/all-hands-ai/openhands:latest

    # 2. Configure claude-haiku-4-5 via Anthropic API

    # 3. Run evaluations
    python3 experiments/run_eval_v2.py --tasks 164
    python3 experiments/swe_eval_proper.py --tasks 30
    python3 experiments/ablation_study.py --tasks 20

> Reproducibility: the study used the unpinned :latest Docker tag and single-pass runs with unrecorded temperature/seed — stated openly in the paper's Limitations.

---

## Key Literature

| Paper | Year | Reference |
|---|---|---|
| MetaGPT | 2024 | arXiv:2308.00352 |
| ChatDev | 2024 | ACL 2024 |
| MapCoder | 2024 | ACL 2024 |
| Magentic-One | 2025 | arXiv:2411.04468 |
| PotPie | 2025 | GitHub |
| OpenHands | 2024 | arXiv:2407.16741 |
| Agentless | 2024 | arXiv:2407.01489 |
| HumanEval | 2021 | arXiv:2107.03374 |
| SWE-bench | 2024 | ICLR 2024 |

---

## Contact

**Shahab Ali** | ID: 503271 | Group: J4132
ITMO University — Faculty of AI Technologies (FATII)
Supervisor: Professor Sergey Kovalchuk
