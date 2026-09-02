![Status](https://img.shields.io/badge/Status-Active-success)
![Institution](https://img.shields.io/badge/Institution-ITMO_University-blue)
![Framework](https://img.shields.io/badge/Framework-OpenHands_CodeAct-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Model](https://img.shields.io/badge/Model-claude--haiku--4--5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Multi-Agent LLM Evaluation for Software Engineering

**ITMO University | Faculty of Artificial Intelligence Technologies (FATII)**
**Student:** Shahab Ali | ID: 503271 | Group: J4132
**Supervisor:** Professor Sergey Kovalchuk | 2025-2026

---

## Project Overview

This research evaluates how different multi-agent role configurations affect LLM agent performance on standard software engineering benchmarks. The same underlying model is tested across four role configurations to isolate the effect of role assignment from model capability.

**Total experimental runs: 773**
- HumanEval: 164 tasks x 4 configurations = 656 runs
- SWE-bench Lite: 30 tasks x 4 configurations = 120 runs
- Prompt Ablation (Q1): 20 tasks x 7 variants = 140 runs

---

## Two Semester Journey

### Semester 1 (Theory) — Systematic Literature Review

Following PRISMA guidelines, analyzed 19 state-of-the-art papers (2023-2025).

**Search Keywords:** ("Large Language Model" OR "LLM") AND ("Software Engineering") AND ("Multi-agent" OR "Role-based")

**Built a 7-layer Agent Role Taxonomy:**

```
Agent Roles — 7 Layers
├── 1. Orchestration      → Manager, Supervisor, Project Coordinator
├── 2. Analysis/Planning  → Planner, Requirement Analyst
├── 3. Design             → Architect, System Modeler
├── 4. Implementation     → Coder, Executor
├── 5. Quality Assurance  → Tester, Reviewer, Debugger (9 papers - highest)
├── 6. Knowledge          → KG Curator, Documentation Writer (8 papers)
└── 7. Operations         → Tooling, Environment Interface (6 papers)
```

**Key Frameworks Analyzed:**

| Framework | Year | Core Roles | Key Technique |
|---|---|---|---|
| MetaGPT | 2024 | PM, Architect, Engineer, QA | SOPs to guide workflows |
| ChatDev | 2024 | CEO, CTO, Programmer, Reviewer | Waterfall + Chat Chain |
| Magentic-One | 2025 | Manager, Specialist Agents | Manager-Worker orchestration |
| PotPie | 2025 | Debugger, Tester, KG Curator | Knowledge Graph grounding |

**Key Trend:** Shift from code Generation to Verification — QA layer dominates (9/19 papers).

---

### Semester 2 (Initial Experiments) — Framework Evaluation

Tested local vs cloud LLMs within OpenHands CodeAct framework.

**Phase 1: HumanEval (15 tasks)**

| Config | LLM | Pass% |
|---|---|---|
| Single Coder | Local 7B | 0% |
| Coder+Tester | Local 7B | 0% |
| Single Coder | Cloud 120B | 100% |
| Coder+Tester | Cloud 120B | 100% |

**Phase 2: SWE-bench (6 tasks)**

| Condition | Pass Rate |
|---|---|
| Without Anti-Paralysis instruction | 33.3% |
| With Anti-Paralysis instruction | 100% |

**Key Discoveries:**

**1. Self-Healing Phenomenon:** 120B model autonomously recovered from errors in 9/10 cases (90% recovery rate).

**2. Agentic Paralysis:** Complex tasks induced reasoning loops where agent correctly identified next step but failed to execute.

**3. Anti-Paralysis Prompt:** Single meta-cognitive constraint increased SWE-bench pass rate from 33.3% to 100%.

**Failure Taxonomy (10 Types Documented):**

| # | Failure Type | Recovery |
|---|---|---|
| 1 | XML Schema Error | Self-Heal |
| 2 | Context Collapse | None |
| 3 | System Prompt Bleed | None |
| 4 | File Conflict | Pivot |
| 5 | Placeholder Hallucination | Self-Heal |
| 6 | Agentic Paralysis | None |
| 7 | Verbose Agentic Paralysis | Partial |
| 8 | Chain Failure | None |
| 9 | Environment Dependency | None |
| 10 | File Not Found | Exploration |

---

## Post-Defense Extended Experiments (2026)

After defense rejection for insufficient sample size, experiments were massively expanded using a fully automated evaluation pipeline.

**Setup:**

| Component | Details |
|---|---|
| Framework | OpenHands CodeAct |
| Model | claude-haiku-4-5 (SAME for ALL configs) |
| HumanEval | 164 tasks (full benchmark) |
| SWE-bench | 30 tasks (SWE-bench Lite) |
| Ablation | 20 tasks x 7 prompt variants |
| Timeout | 600 seconds per config per task |
| Total Runs | 773 |

**Four Role Configurations:**

| Configuration | Description |
|---|---|
| Baseline (No Roles) | Direct task, no role assignment |
| Coder Only | Single Coder agent with format constraint |
| Coder + Tester | Two roles: Coder writes, Tester verifies |
| Manager + Coder + Tester | Three roles: Manager plans, Coder implements, Tester verifies |

---

### HumanEval Results (164 tasks, metric: pass@1)

pass@1 = agent passes ALL official test cases on first attempt.

| Configuration | Tasks | Pass | Fail | pass@1 | vs Baseline |
|---|---|---|---|---|---|
| Baseline (No Roles) | 161 | 149 | 12 | 92.5% | — |
| Coder Only | 164 | 155 | 9 | 94.5% | +2.0 pp |
| Coder + Tester | 164 | 152 | 12 | 92.7% | +0.2 pp |
| **Manager+Coder+Tester** | **164** | **156** | **8** | **95.1%** | **+2.6 pp** |

**Failure Analysis:**

| Configuration | SyntaxError | AssertionError | NameError | EmptyCode |
|---|---|---|---|---|
| Baseline | 4 | 4 | 3 | 1 |
| Coder Only | 0 | 3 | 5 | 1 |
| Coder + Tester | 0 | 6 | 4 | 2 |
| Manager+Coder+Tester | 0 | 3 | 4 | 1 |

---

### SWE-bench Lite Results (30 real GitHub tasks, metric: resolve_rate)

resolve_rate = agent modified correct source files, verified via git diff against reference patch.

| Configuration | Tasks | Resolved | Failed | Rate | Avg Time | Resolved Avg |
|---|---|---|---|---|---|---|
| Baseline (No Roles) | 30 | 22 | 8 | 73.3% | 296s | 168.9s |
| **Coder Only** | **30** | **25** | **5** | **83.3%** | **232s** | **151.5s** |
| Coder + Tester | 30 | 20 | 10 | 66.7% | 331s | 174.2s |
| Manager+Coder+Tester | 30 | 24 | 6 | 80.0% | 295s | 206.1s |

> All SWE-bench failures are timeouts (600s limit), not logic errors.

**Cross-Benchmark Comparison:**

| Configuration | HumanEval | SWE-bench | vs Baseline (HE) | vs Baseline (SWE) |
|---|---|---|---|---|
| Baseline | 92.5% | 73.3% | — | — |
| Coder Only | 94.5% | 83.3% | +2.0 pp | +10.0 pp |
| Coder + Tester | 92.7% | 66.7% | +0.2 pp | -6.6 pp |
| Manager+Coder+Tester | 95.1% | 80.0% | +2.6 pp | +6.7 pp |

---

### Research Question 1 — Prompt Ablation Study

**Question:** What details in the role prompt most influence agent performance?

**Method:** 7 prompt variants tested on 20 tasks (140 runs total).

| Variant | Components | pass@1 |
|---|---|---|
| Baseline | No role | 95.0% |
| Coder A | Identity only: "You are a Coder" | 0.0% |
| Coder B | Identity + Responsibility | 0.0% |
| **Coder C** | **Identity + Responsibility + Format** | **100.0%** |
| Full A | All role titles only | 0.0% |
| Full B | All titles + responsibilities | 0.0% |
| Full C | All full prompts with format | 95.0% |

**Finding:** The output format constraint is the single critical component. Without "Output ONLY the function, no explanation" — agents produce unparseable output regardless of role identity. Role identity and responsibility alone have zero effect.

**Why it works:** LLMs are trained on data where code is accompanied by explanations. Without the format constraint, the model's default output distribution produces verbose responses. The format instruction shifts this distribution toward code-only output.

---

### Research Question 2 — State Prediction Method

**Question:** How can we select the appropriate role for a given task scientifically?

**Method:** Decision Tree classifier trained on 12 task features (state representation) predicts optimal role configuration.

**State Features:**
- Structural: num_lines, num_words, num_chars, indentation
- Semantic: type_count, uses_list, uses_dict, uses_optional
- Complexity: examples, complex_words, return_hints, docstring_blocks

**Learned Decision Rules:**

```
|--- type_count <= 9.5
|   |--- num_words <= 217.0  -->  baseline  (simple task)
|   |--- num_words > 217.0   -->  coder     (long description)
|--- type_count > 9.5
|   |--- examples <= 1.0     -->  baseline
|   |--- examples > 1.0      -->  coder     (complex + examples)

5-fold cross-validation accuracy: 86.0%
```

**Results:**

| Method | pass@1 | Type |
|---|---|---|
| Baseline | 92.5% | Fixed |
| Coder Only | 94.5% | Fixed |
| Manager+Coder+Tester | 95.1% | Fixed |
| **State Predictor (DT)** | **93.3%** | **Scientific Method** |

**Feature Importance:**

| Feature | Importance | Meaning |
|---|---|---|
| type_count | 0.267 | Number of type annotations |
| num_words | 0.217 | Task description length |
| examples | 0.159 | Number of docstring examples |
| uses_list | 0.154 | Whether List type is used |
| num_lines | 0.153 | Prompt length in lines |

**Task Difficulty Analysis:**

| Category | Count | Note |
|---|---|---|
| Tasks where config selection matters | 6 (3.7%) | Only 1 config passes |
| Tasks where all configs work equally | 158 (96.3%) | Multiple configs pass |

**Scientific Finding:** For 96.3% of tasks, all role configurations pass equally. Config selection only matters for the hardest 3.7% of tasks — revealing that role configuration acts as a safety mechanism for boundary cases, not a general performance booster.

---

## Repository Structure

```
/experiments
  run_eval_v2.py               - HumanEval automated evaluation script
  swe_eval_proper.py           - SWE-bench evaluation with real repo cloning
  ablation_study.py            - Q1 prompt ablation study script
  eval_results.jsonl           - HumanEval raw results (653 runs)
  eval_summary_FINAL.csv       - HumanEval summary table
  swe_results_FINAL.jsonl      - SWE-bench raw results (120 runs)
  swe_summary_FINAL.csv        - SWE-bench summary table
  ablation_results_FINAL.jsonl - Q1 ablation results (140 runs)
  ablation_summary.csv         - Q1 summary table
  q2_state_prediction.txt      - Q2 state predictor results
  q2_complete_analysis.txt     - Q2 full analysis with decision tree rules
/taxonomy                      - Semester 1 SLR and 7-layer taxonomy
/docs                          - Research paper and presentations
/reports                       - Weekly progress reports
```

---

## Replication

```bash
# 1. Start OpenHands
docker run -d --name openhands-eval --memory="4g" \
    -e SANDBOX_VOLUMES="$(pwd)/workspace:/workspace:rw" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -p 3000:3000 \
    ghcr.io/all-hands-ai/openhands:latest

# 2. Configure: claude-haiku-4-5 via Anthropic API

# 3. Run HumanEval (164 tasks)
python3 experiments/run_eval_v2.py --tasks 164

# 4. Run SWE-bench (30 tasks)
python3 experiments/swe_eval_proper.py --tasks 30

# 5. Run Prompt Ablation Study
python3 experiments/ablation_study.py --tasks 20
```

---

## Key Literature

| Paper | Year | Key Contribution |
|---|---|---|
| MetaGPT | 2024 | SOPs for multi-agent workflows |
| ChatDev | 2024 | Waterfall model with chat chain |
| MapCoder | 2024 | Multi-agent competitive coding |
| Magentic-One | 2025 | Manager-worker orchestration |
| PotPie | 2025 | Knowledge graph grounding |

---

## Contact

**Student:** Shahab Ali | ID: 503271 | Group: J4132
**University:** ITMO University — Faculty of AI Technologies (FATII)
**Supervisor:** Professor Sergey Kovalchuk
