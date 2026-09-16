![Status](https://img.shields.io/badge/Status-Active-success)
![Institution](https://img.shields.io/badge/Institution-ITMO_University-blue)
![Framework](https://img.shields.io/badge/Framework-OpenHands_CodeAct-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Model](https://img.shields.io/badge/Model-claude--haiku--4--5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Agentic Role Bounding and Optimization in Multi-Agent LLM Systems for Software Engineering

**ITMO University | Faculty of Artificial Intelligence Technologies (FATII)**
**Student:** Shahab Ali | ID: 503271 | Group: J4132
**Supervisor:** Professor Sergey Kovalchuk | 2025–2026

---

## Research Summary

This project studies how agent roles in LLM-based software engineering systems can be defined operationally, selected according to task state, and evaluated independently of final task success.

The research developed through four stages:

**Role Taxonomy → Role Bounding → State-Driven Selection → Architecture Measurement**

### Final Research Questions

**RQ1 — Role Exposure and Optimization**

How can an agent role be formally defined so that its effect is controllable, and how can an appropriate role configuration be selected according to task state?

**RQ2 — Architecture Measurement**

How can the intrinsic efficiency and stability of an agent-role architecture be measured independently of final task success?

---

## Experimental Scope

| Component | Count |
|---|---:|
| HumanEval: 164 tasks × 4 configurations | 656 |
| SWE-bench Lite: 30 tasks × 4 configurations | 120 |
| Prompt ablation: 20 tasks × 7 variants | 140 |
| **Phase 2 total** | **916** |
| Phase 1 exploratory runs | 21 |
| **All-time total** | **937** |

Phase 2 holds the model constant and varies the role configuration.

**Model:** `claude-haiku-4-5`
**Framework:** OpenHands CodeAct
**HumanEval timeout:** 400 s
**SWE-bench timeout:** 600 s

---

## Main Findings

| Finding | Observed result |
|---|---|
| Role identity only | Coder A: 0/20 in the prompt ablation |
| Identity + responsibility | Coder B: 0/20 |
| Identity + responsibility + explicit output constraint | Coder C: 20/20 |
| HumanEval configuration sensitivity | 19 of 164 tasks change outcome across configurations |
| HumanEval architecture-insensitive tasks | 145 of 164 |
| Learned selector | 94.53% CV accuracy |
| Majority-class policy | 95.13% CV accuracy |
| Selector margin | −0.61 percentage points |
| SWE-bench Coder+Tester vs Coder runtime | +99.2 s/task observed mean difference |

These findings are specific to the experimental setting used here and are not claimed to establish universal superiority of any role configuration.

---

## Semester 1 — Prior Foundation: Seven-Layer Role Taxonomy

A structured review of 19 sources produced a seven-layer taxonomy of agent roles.

The categories are non-exclusive: one source may contribute to multiple role families.

```text
Agent Roles — 7 Layers
├── 1. Orchestration         5 sources
├── 2. Analysis & Planning   5 sources
├── 3. Design                4 sources
├── 4. Implementation        5 sources
├── 5. Quality Assurance     9 sources
├── 6. Knowledge & Docs      8 sources
└── 7. Operations & Tooling  6 sources
```

Quality Assurance is the most represented role family in this review.

The review motivated the next question: roles are commonly described by names and responsibilities, but their operational boundaries are rarely isolated experimentally.

---

## Phase 1 — Exploratory Work

Phase 1 contained 21 early exploratory runs.

This phase preceded the controlled redesign and did not use structured event logging. Its observations are therefore treated as exploratory rather than as controlled benchmark results.

Observed phenomena included:

- **Autonomous recovery:** 9 of 10 observed error events were followed by successful completion without human intervention.
- **Agentic Paralysis:** the agent states the next action but fails to issue the corresponding tool call.
- **Verbose Paralysis:** one observed run repeated similar reasoning 200+ times before a rate-limit / chain failure.
- **Ten failure types:** catalogued qualitatively from the exploratory runs.

An anti-paralysis instruction was also tested on different SWE-bench tasks:

```text
If any single action fails or repeats more than 3 times,
STOP immediately.
Run: ls /workspace/ to reorient yourself.
Maximum 3 attempts per action.
```

The observed change was 1/3 resolved before and 3/3 after, but the tasks were different. This is reported only as a motivating observation, not as a controlled causal comparison.

---

## Phase 2 — Controlled Experimental Program

The Phase 2 redesign addressed the main confound in Phase 1 by holding the model constant across configurations.

### Four Main Configurations

1. Baseline
2. Coder
3. Coder + Tester
4. Manager + Coder + Tester

---

## HumanEval Results

Full HumanEval benchmark: 164 tasks × 4 configurations = 656 runs.

| Configuration | Pass | Fail | pass@1 |
|---|---:|---:|---:|
| Baseline | 151 | 13 | 92.1% |
| Coder | 155 | 9 | 94.5% |
| Coder + Tester | 152 | 12 | 92.7% |
| Manager + Coder + Tester | 156 | 8 | 95.1% |

Observed differences are small.

The best-minus-worst difference is 3.0 percentage points.

Baseline is the only configuration that produced SyntaxErrors in this evaluation:

- Baseline: 4 SyntaxErrors
- Coder: 0
- Coder+Tester: 0
- Full system: 0

### Architecture-Sensitive Tasks

Out of 164 HumanEval tasks:

- **145** have identical outcomes across all four configurations.
- **19** are architecture-sensitive.
- **8** are rescued after baseline failure.
- **11** are lost by at least one role configuration.
- **5** are solved by no configuration.

All-fail tasks:

```text
HumanEval/32
HumanEval/38
HumanEval/50
HumanEval/116
HumanEval/145
```

Maximum achievable task success across the observed configurations:

```text
159 / 164 = 96.95%
```

---

## SWE-bench Lite Results

The first 30 SWE-bench Lite tasks were evaluated under all four configurations.

Resolution is based on file-level git-diff overlap against the reference patch, not the official SWE-bench test suite.

| Configuration | Resolved | Failed | Rate | Mean runtime |
|---|---:|---:|---:|---:|
| Baseline | 22 | 8 | 73.3% | 296.0 s |
| Coder | 25 | 5 | 83.3% | 232.1 s |
| Coder + Tester | 20 | 10 | 66.7% | 331.3 s |
| Manager + Coder + Tester | 24 | 6 | 80.0% | 295.2 s |

Observed mean runtime difference:

```text
Coder+Tester − Coder = +99.2 s/task
```

All six pairwise McNemar comparisons produced:

```text
p > 0.05
```

The resolve-rate differences are therefore not statistically significant in this sample.

Official SWE-bench evaluation may produce different results because this study uses an internal file-level criterion.

---

## RQ1a — Constrained Action Space

The proposed role representation is:

```text
R = (A_R, O_R, T_R)
```

where:

- `A_R` = permitted actions
- `O_R` = output/schema constraints
- `T_R` = permitted tools and transitions

For task state `s`:

```text
A_R(s) ⊆ A
```

The current experiments directly evaluate only the output-constraint component `O_R`.

Action and tool/transition constraints remain proposed extensions for future validation.

---

## Prompt Ablation

Seven prompt variants were tested on HumanEval/0–19.

20 tasks × 7 variants = 140 runs.

| Variant | Components | Result |
|---|---|---:|
| Baseline | output constraint only | 19/20 |
| Coder A | identity | 0/20 |
| Coder B | identity + responsibility | 0/20 |
| Coder C | identity + responsibility + output constraint | 20/20 |
| Full A | three role titles | 0/20 |
| Full B | titles + responsibilities | 0/20 |
| Full C | titles + responsibilities + output constraint | 19/20 |

Only the variants carrying an explicit output-format constraint succeeded in this experiment.

Prompt length was not fully controlled and the variants were not token- or length-matched.

However, the shortest constrained prompt passes 19/20 while the longest unconstrained prompt passes 0/20, making a length-only explanation unlikely without fully ruling it out.

---

## RQ1b — State-Driven Configuration Selection

Role selection is formulated as:

```text
π(a | s)
```

where:

- `s` = task state
- `a` = selected role configuration

Candidate configurations:

```text
{baseline, coder, coder+tester, full system}
```

### Label Rule

The first passing configuration is selected in the fixed order:

```text
baseline → coder → coder+tester → full system
```

Tasks solved by no configuration default to baseline.

### Class Distribution

| Class | Count |
|---|---:|
| Baseline | 156 |
| Coder | 8 |
| Coder+Tester | 0 |
| Full system | 0 |

### Five-Fold Cross-Validation

| Policy | Classification accuracy |
|---|---:|
| Majority-class policy | 95.13% |
| Decision Tree | 94.53% |
| **Margin** | **−0.61 pp** |

Unrounded means:

```text
Decision Tree : 0.9452651515
Majority      : 0.9513257576
Margin        : −0.606061 pp
```

This is reported as a negative result.

Under this labeling rule, only 8 of 164 tasks receive a non-baseline label, producing severe class imbalance.

### Nonzero Feature Importances

| Feature | Importance |
|---|---:|
| type_count | 0.344817 |
| num_lines | 0.277943 |
| num_words | 0.275645 |
| uses_list | 0.060159 |
| complex_words | 0.041437 |

The remaining seven features have zero importance in the fitted tree.

---

## RQ2 — Architecture-Level Measurement

Three architecture-level metrics are proposed.

### Coordination Friction

```text
F_coord = T_coord / T_total
```

Share of the token budget spent on coordination.

**Status:** proposed.

The observed +99.2 s/task runtime difference between Coder+Tester and Coder provides motivation for measuring coordination cost, but it is not itself a measurement of `F_coord`.

### Autonomous Recovery Rate

```text
R_auto = E_recovered / E_total
```

**Exploratory Phase 1 value:**

```text
9 / 10 = 0.90
```

This value was reconstructed from qualitative weekly reports rather than structured event logs.

### Boundary Violation Rate

```text
V_boundary =
N_violations /
N_role-governed_actions
```

**Status:** proposed.

The Phase 1 failure taxonomy provides candidate events, but no automated violation counter was implemented.

---

## Reproducibility Record

| Item | Value |
|---|---|
| Model | claude-haiku-4-5 via Anthropic API |
| Main comparison | same model across all four configurations |
| Framework | OpenHands CodeAct |
| Docker image | `ghcr.io/all-hands-ai/openhands:latest` |
| Docker image status | unpinned |
| HumanEval | all 164 tasks |
| HumanEval timeout | 400 s |
| SWE-bench Lite | first 30 tasks |
| SWE timeout | 600 s |
| Ablation | HumanEval/0–19 |
| Repeats | single run per condition |
| Temperature | not recorded |
| Generation seed | not recorded |
| Selector | DecisionTreeClassifier(max_depth=4, random_state=42) |
| Cross-validation | 5-fold StratifiedKFold, shuffle=True, random_state=42 |

Exact reproduction is limited by the unpinned Docker image and unrecorded generation temperature/seed.

---

## Repository Structure

```text
experiments/
  run_eval_v2.py
  swe_eval_proper.py
  ablation_study.py

  eval_results.jsonl
  swe_results_FINAL.jsonl
  ablation_results_FINAL.jsonl

analysis/
  mcnemar_tests.py
  rq3_baseline.py
  decisive_tasks.py

taxonomy/
  Semester 1 taxonomy materials

docs/
  research_paper.pdf
  Shahab_Ali_FINAL_Presentation.pptx

reports/
  Phase 1 and progress reports

RESULTS_APPENDIX.md
```

---

## Complete Experimental Appendix

`RESULTS_APPENDIX.md` contains the detailed experimental record generated from the result files, including:

- complete run accounting
- HumanEval configuration results
- architecture-sensitive tasks
- SWE-bench task-level outcomes
- pairwise McNemar tests
- exact prompt-ablation definitions and results
- state-selector analysis
- reproducibility details
- explicitly labeled Phase 1 exploratory observations

---

## Replication

The raw Phase 2 result files and experiment scripts are included in this repository.

The experiments were originally executed through OpenHands CodeAct using `claude-haiku-4-5`.

Example evaluation scripts:

```bash
python3 experiments/run_eval_v2.py
python3 experiments/swe_eval_proper.py
python3 experiments/ablation_study.py
```

The precise command-line options should be verified from the corresponding script before rerunning.

---

## Selected Literature

| Work | Year | Reference |
|---|---:|---|
| MetaGPT | 2024 | arXiv:2308.00352 |
| ChatDev | 2024 | ACL 2024 |
| MapCoder | 2024 | ACL 2024 |
| Magentic-One | 2025 | arXiv:2411.04468 |
| PotPie | 2025 | GitHub |
| OpenHands | 2024 | arXiv:2407.16741 |
| Agentless | 2024 | arXiv:2407.01489 |
| HumanEval | 2021 | arXiv:2107.03374 |
| SWE-bench | 2024 | ICLR 2024 |

This is a selected list rather than the complete 19-source review matrix.

---

## Final Paper

**Title:** Agentic Role Bounding and Optimization in Multi-Agent LLM Systems for Software Engineering

**File:** `docs/research_paper.pdf`

---

## Contact

**Shahab Ali**
ID: 503271 · Group: J4132
ITMO University · Faculty of Artificial Intelligence Technologies
Supervisor: Professor Sergey Kovalchuk

---

## License

MIT License
