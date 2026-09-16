# Complete Experimental Appendix

Multi-Agent LLM Role Configurations for Software Engineering
Shahab Ali · ITMO University · Student ID 503271 · Group J4132
Supervisor: Prof. Sergey Kovalchuk

Phase 2 quantitative results below are computed directly from the tracked result files. Phase 1 observations are manually documented from qualitative weekly reports and are explicitly marked exploratory.

---

## A. Run accounting

| Component | Design | Records |
|---|---|---:|
| HumanEval | 164 × 4 | 656 |
| SWE-bench Lite | 30 × 4 | 120 |
| Prompt ablation | 20 × 7 | 140 |
| **Phase 2 total** | | **916** |
| Phase 1 (exploratory; no structured event log) | manually documented | 21 |
| **All-time total** | | **937** |

Unique HumanEval task×config pairs: **656**. Duplicate records: **0**.

## B. HumanEval — 164 tasks, pass@1

| Configuration | Pass | Fail | n | pass@1 |
|---|---:|---:|---:|---:|
| Baseline | 151 | 13 | 164 | 92.1% |
| Coder | 155 | 9 | 164 | 94.5% |
| Coder+Tester | 152 | 12 | 164 | 92.7% |
| Manager+Coder+Tester | 156 | 8 | 164 | 95.1% |

**Failure breakdown**

| Configuration | AssertionError | EmptyCode/Other | NameError | SyntaxError |
|---|---:|---:|---:|---:|
| Baseline | 4 | 1 | 4 | 4 |
| Coder | 3 | 1 | 5 | 0 |
| Coder+Tester | 6 | 2 | 4 | 0 |
| Manager+Coder+Tester | 3 | 1 | 4 | 0 |

**Architecture-sensitive tasks:** 19 of 164 (the other 145 give identical outcomes).

| Task | Baseline | Coder | Coder+Tester | Manager+Coder+Tester | Category |
|---|---|---|---|---|---|
| HumanEval/4 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/7 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/8 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/10 | FAIL | PASS | FAIL | PASS | rescued after baseline failure |
| HumanEval/83 | PASS | PASS | PASS | FAIL | lost by a role |
| HumanEval/85 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/104 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/106 | PASS | PASS | FAIL | PASS | lost by a role |
| HumanEval/108 | PASS | PASS | FAIL | PASS | lost by a role |
| HumanEval/113 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/129 | FAIL | PASS | PASS | PASS | rescued after baseline failure |
| HumanEval/132 | PASS | PASS | PASS | FAIL | lost by a role |
| HumanEval/134 | PASS | PASS | FAIL | PASS | lost by a role |
| HumanEval/139 | PASS | PASS | FAIL | PASS | lost by a role |
| HumanEval/141 | PASS | PASS | FAIL | PASS | lost by a role |
| HumanEval/147 | PASS | FAIL | PASS | PASS | lost by a role |
| HumanEval/154 | PASS | FAIL | FAIL | FAIL | lost by a role |
| HumanEval/156 | PASS | FAIL | PASS | PASS | lost by a role |
| HumanEval/162 | PASS | FAIL | PASS | PASS | lost by a role |

Rescued after baseline failure: **8** · Lost by a role: **11**

**Solved by no configuration (5):** HumanEval/32, HumanEval/38, HumanEval/50, HumanEval/116, HumanEval/145

Maximum achievable task success across the observed configurations: 159/164 = 96.95%

## C. SWE-bench Lite — 30 repository tasks

Resolution uses **file-level diff overlap against the reference patch**, not the official SWE-bench test suite. Rates are comparable within this study only.

| Configuration | Resolved | Failed | Rate | Mean runtime |
|---|---:|---:|---:|---:|
| Baseline | 22 | 8 | 73.3% | 296.0 s |
| Coder | 25 | 5 | 83.3% | 232.1 s |
| Coder+Tester | 20 | 10 | 66.7% | 331.3 s |
| Manager+Coder+Tester | 24 | 6 | 80.0% | 295.2 s |

Observed mean runtime difference, Coder+Tester vs Coder: **+99.2 s per task**.

**Task IDs (30), first-N slice of SWE-bench Lite**

| # | Instance | Baseline | Coder | Coder+Tester | Manager+Coder+Tester |
|---:|---|---|---|---|---|
| 1 | `astropy__astropy-12907` | PASS | PASS | PASS | PASS |
| 2 | `astropy__astropy-14182` | PASS | FAIL | FAIL | PASS |
| 3 | `astropy__astropy-14365` | PASS | PASS | PASS | FAIL |
| 4 | `astropy__astropy-14995` | FAIL | FAIL | FAIL | PASS |
| 5 | `astropy__astropy-6938` | FAIL | PASS | PASS | PASS |
| 6 | `astropy__astropy-7746` | PASS | PASS | FAIL | PASS |
| 7 | `django__django-10914` | PASS | PASS | FAIL | PASS |
| 8 | `django__django-10924` | FAIL | FAIL | FAIL | FAIL |
| 9 | `django__django-11001` | FAIL | PASS | FAIL | PASS |
| 10 | `django__django-11019` | PASS | PASS | PASS | PASS |
| 11 | `django__django-11039` | PASS | FAIL | PASS | PASS |
| 12 | `django__django-11049` | PASS | FAIL | PASS | FAIL |
| 13 | `django__django-11099` | FAIL | PASS | FAIL | PASS |
| 14 | `django__django-11133` | PASS | PASS | PASS | PASS |
| 15 | `django__django-11179` | PASS | PASS | PASS | FAIL |
| 16 | `django__django-11283` | PASS | PASS | FAIL | PASS |
| 17 | `django__django-11422` | PASS | PASS | PASS | PASS |
| 18 | `django__django-11564` | PASS | PASS | PASS | FAIL |
| 19 | `django__django-11583` | PASS | PASS | FAIL | FAIL |
| 20 | `django__django-11620` | PASS | PASS | PASS | PASS |
| 21 | `django__django-11630` | PASS | PASS | PASS | PASS |
| 22 | `django__django-11742` | PASS | PASS | PASS | PASS |
| 23 | `django__django-11797` | PASS | PASS | PASS | PASS |
| 24 | `django__django-11815` | FAIL | PASS | PASS | PASS |
| 25 | `django__django-11848` | PASS | PASS | PASS | PASS |
| 26 | `django__django-11905` | PASS | PASS | PASS | PASS |
| 27 | `django__django-11910` | PASS | PASS | PASS | PASS |
| 28 | `django__django-11964` | PASS | PASS | PASS | PASS |
| 29 | `django__django-11999` | FAIL | PASS | PASS | PASS |
| 30 | `django__django-12113` | FAIL | PASS | FAIL | PASS |

**Pairwise McNemar tests**

| Comparison | b01 | b10 | Discordant | p | Significant |
|---|---:|---:|---:|---:|---|
| Baseline vs Coder | 6 | 3 | 9 | 0.5078 | no |
| Baseline vs Coder+Tester | 3 | 5 | 8 | 0.7266 | no |
| Baseline vs Manager+Coder+Tester | 7 | 5 | 12 | 0.7744 | no |
| Coder vs Coder+Tester | 2 | 7 | 9 | 0.1797 | no |
| Coder vs Manager+Coder+Tester | 3 | 4 | 7 | 1.0000 | no |
| Coder+Tester vs Manager+Coder+Tester | 8 | 4 | 12 | 0.3877 | no |

## D. Prompt ablation — 7 variants × 20 tasks

**Prompts, read verbatim from `experiments/ablation_study.py`**

- **baseline** — Baseline (No Role)
  `Complete this Python function. Output ONLY the complete function code:`
- **coder_A** — Coder A: Identity Only
  `You are a Coder agent.`
- **coder_B** — Coder B: Identity + Responsibility
  `You are a Coder agent. Your ONLY job is to write correct Python code.`
- **coder_C** — Coder C: Full Prompt
  `You are a Coder agent. Your ONLY job is to write correct Python code. Output ONLY the complete function, no explanation, no markdown:`
- **full_A** — Full A: Titles Only
  `You are a multi-agent system: MANAGER, CODER, TESTER.`
- **full_B** — Full B: Titles + Responsibilities
  `You are a multi-agent system: MANAGER: Plan the solution. CODER: Write the Python function. TESTER: Verify correctness.`
- **full_C** — Full C: Full Prompt
  `You are a multi-agent system: MANAGER: Create a step-by-step logic plan. CODER: Implement the function from the plan. TESTER: Verify and fix any bugs. Output ONLY the final Python function, no explanation, no markdown:`

| Variant | Pass | n | pass@1 |
|---|---:|---:|---:|
| baseline | 19 | 20 | 95.0% |
| coder_A | 0 | 20 | 0.0% |
| coder_B | 0 | 20 | 0.0% |
| coder_C | 20 | 20 | 100.0% |
| full_A | 0 | 20 | 0.0% |
| full_B | 0 | 20 | 0.0% |
| full_C | 19 | 20 | 95.0% |

Tasks used (20): HumanEval/0, HumanEval/1, HumanEval/2, HumanEval/3, HumanEval/4, HumanEval/5, HumanEval/6, HumanEval/7, HumanEval/8, HumanEval/9, HumanEval/10, HumanEval/11, HumanEval/12, HumanEval/13, HumanEval/14, HumanEval/15, HumanEval/16, HumanEval/17, HumanEval/18, HumanEval/19

Variants were **not** token- or length-matched. The shortest constrained prompt passes 19/20 while the longest unconstrained prompt passes 0/20, making a length-only explanation unlikely without fully controlling for it.

## E. State prediction (RQ1b)

**Label rule:** first passing configuration in the fixed order baseline → coder → coder+tester → full system; tasks solved by no configuration default to baseline.

**Class distribution:** baseline 156, coder 8

| Policy | Classification accuracy |
|---|---:|
| Majority-class | 95.13% |
| Decision tree (depth 4, seed 42) | 94.53% |
| **Margin** | **-0.61 pp** |

Decision-tree fold scores: 0.9393939394, 0.9393939394, 0.9696969697, 0.9090909091, 0.9687500000

Majority-policy fold scores: 0.9696969697, 0.9393939394, 0.9393939394, 0.9393939394, 0.9687500000

**Feature importances**

| Feature | Importance |
|---|---:|
| type_count | 0.344817 |
| num_lines | 0.277943 |
| num_words | 0.275645 |
| uses_list | 0.060159 |
| complex_words | 0.041437 |
| num_chars | 0.000000 |
| return_hints | 0.000000 |
| uses_dict | 0.000000 |
| uses_optional | 0.000000 |
| docstring_blocks | 0.000000 |
| examples | 0.000000 |
| indentation | 0.000000 |

**Learned tree**

```text
|--- type_count <= 9.50
|   |--- num_words <= 217.00
|   |   |--- complex_words <= 4.50
|   |   |   |--- num_lines <= 11.50
|   |   |   |   |--- class: baseline
|   |   |   |--- num_lines >  11.50
|   |   |   |   |--- class: baseline
|   |   |--- complex_words >  4.50
|   |   |   |--- uses_list <= 1.00
|   |   |   |   |--- class: baseline
|   |   |   |--- uses_list >  1.00
|   |   |   |   |--- class: baseline
|   |--- num_words >  217.00
|   |   |--- class: coder
|--- type_count >  9.50
|   |--- num_lines <= 18.50
|   |   |--- class: coder
|   |--- num_lines >  18.50
|   |   |--- class: baseline
```

The learned selector does not beat the trivial majority-class policy. Under the first-success labeling rule, only **8 of 164** tasks receive a non-baseline label, producing severe class imbalance. Separately, **19 of 164** tasks are architecture-sensitive in the broader sense that at least one configuration changes the outcome. This is reported as a negative result.

## F. Reproducibility record

| Item | Value |
|---|---|
| Model | claude-haiku-4-5 (Anthropic API), identical in all main configurations |
| Framework | OpenHands CodeAct in Docker |
| Docker image | `ghcr.io/all-hands-ai/openhands:latest` — **unpinned** |
| HumanEval task selection | all 164 tasks |
| HumanEval timeout | 400 s per task |
| HumanEval evaluation | in-process exec + official `check()` |
| SWE-bench Lite task selection | first 30 tasks |
| SWE-bench timeout | 600 s per task |
| SWE-bench evaluation | file-level git diff overlap vs reference patch |
| Ablation task selection | HumanEval/0–19 |
| Repeats | single run per condition |
| Temperature | **not recorded** |
| Random seed (generation) | **not recorded** |
| Selector seed | random_state=42, 5-fold stratified CV |

**Known limitations.** Single run per condition, so there is no variance estimate across repeated generations. Temperature and generation seed were not recorded, and the Docker image tag was unpinned. SWE-bench rates use an internal file-level criterion rather than the official test suite. The main evaluation uses one model family, and the ablation covers 20 tasks and one constraint type.

## G. Phase 1 (exploratory, 21 runs)

Phase 1 preceded the redesign and had no structured event logging. The following values are manually documented from qualitative weekly reports and are **not** controlled Phase 2 benchmark results.

- **Autonomous recovery:** 9 of 10 observed error events were followed by successful task completion without human intervention (`R_auto = 0.90`). Reconstructed from weekly reports.
- **Agentic Paralysis:** the agent states the next action in reasoning but does not issue the corresponding tool call.
- **Verbose paralysis case:** one run repeated similar reasoning 200+ times before a rate-limit / chain failure.
- **Anti-paralysis instruction:** "If any single action fails or repeats more than 3 times, STOP immediately. Run: ls /workspace/ to reorient yourself. Maximum 3 attempts per action." Observed 1/3 → 3/3 on six **different** tasks. This is a motivating observation, not a controlled causal comparison.
- **Ten-type failure taxonomy:** catalogued qualitatively; types 1, 3 and 5 are candidate boundary-violation events for the proposed `V_boundary` metric.
