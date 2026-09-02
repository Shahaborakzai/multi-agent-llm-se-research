# Multi-Agent LLM Evaluation for Software Engineering

**ITMO University | FATII | Student:** Shahab Ali | ID: 503271 | Group: J4132
**Supervisor:** Professor Sergey Kovalchuk | 2025-2026

## Total experimental runs: 773

- HumanEval: 164 tasks x 4 configs = 656 runs
- SWE-bench Lite: 30 tasks x 4 configs = 120 runs  
- Prompt Ablation Q1: 20 tasks x 7 variants = 140 runs

## HumanEval Results (pass@1)

| Configuration | pass@1 |
|---|---|
| Baseline | 92.5% |
| Coder Only | 94.5% |
| Coder + Tester | 92.7% |
| Manager+Coder+Tester | 95.1% |

## SWE-bench Lite Results (resolve_rate)

| Configuration | Rate | Avg Time |
|---|---|---|
| Baseline | 73.3% | 296s |
| Coder Only | 83.3% | 232s |
| Coder + Tester | 66.7% | 331s |
| Manager+Coder+Tester | 80.0% | 295s |

## Q1 Finding
Output format constraint is the critical component. Without it: 0% pass rate.

## Q2 Finding  
Decision Tree state predictor achieves 93.3% with 86% CV accuracy.
Top features: type_count, num_words, examples.
