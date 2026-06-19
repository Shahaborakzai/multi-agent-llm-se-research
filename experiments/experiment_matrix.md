# Complete Experiment Results Matrix

## HumanEval Results (#1–15)

| Task | Config | LLM | Setup | Result | Error | Self-Healed |
|------|--------|-----|-------|--------|-------|-------------|
| #1  | 1 | 7B   | A |  FAIL | Core Collapse | No |
| #2  | 3 | 120B | A |  FAIL | security_risk | No |
| #3  | 4 | 120B | B |  PASS | None | N/A |
| #4  | 3 | 120B | A |  PASS | None | N/A |
| #5  | 3 | 120B | A |  PASS | None | N/A |
| #6  | 4 | 120B | B |  PASS | security_risk |  Yes |
| #7  | 3 | 120B | A |  PASS | security_risk |  Yes |
| #8  | 4 | 120B | B |  PASS | security_risk |  Yes |
| #9  | 3 | 120B | A |  PASS | File Conflict |  Yes |
| #10 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #11 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #12 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #13 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #14 | 4 | 120B | B |  PASS | Placeholder Hallucination |  Yes |
| #15 | 4 | 120B | B |  PASS | security_risk |  Yes |

## HumanEval Summary by Configuration

| Config | LLM | Role | Tasks | Pass% | Crash% | Self-Heal% |
|--------|-----|------|-------|-------|--------|------------|
| 1 | Local 7B   | Single Coder  | 5  | 0%    | 100% | 0%   |
| 2 | Local 7B   | Coder+Tester  | 5  | 0%    | 100% | 0%   |
| 3 | Cloud 120B | Single Coder  | 5  | 100%  | 0%   | 100% |
| 4 | Cloud 120B | Coder+Tester  | 10 | 100%  | 0%   | 100% |

## SWE-bench Results (#1–6)

| Task | Files | Anti-Paralysis | Result | Key Finding |
|------|-------|---------------|--------|-------------|
| SWE #1 | calculator + app | No  |  PASS | Agentic Loop |
| SWE #2 | app.py           | No  |  FAIL | Env Dependency |
| SWE #3 | calculator.py    | No  |  FAIL | Chain Failure |
| SWE #4 | math_utils       | Yes |  PASS | Perfect 8/8 |
| SWE #5 | humaneval_results| Yes |  PASS | Perfect 11/11 |
| SWE #6 | calculator ext.  | Yes |  PASS | Recovered |

## Anti-Paralysis Impact

| Condition | Pass Rate |
|-----------|-----------|
| Without instruction | 33.3% |
| With instruction    | 100%  |

## Overall Statistics

| Metric | Value |
|--------|-------|
| Total runs | 21 |
| Overall pass rate | 71.4% |
| 7B pass rate | 0% |
| 120B pass rate | 78.9% |
| Self-Healing rate | 90% |
| Failure types | 10 |
| New phenomena | 4 |
