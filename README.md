![Status](https://img.shields.io/badge/Status-Complete-success)
![Institution](https://img.shields.io/badge/Institution-ITMO_University-blue)
![Framework](https://img.shields.io/badge/Framework-OpenHands-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Multi-Agent LLM Evaluation for Software Engineering

**ITMO University | Faculty of AI Technologies (FATII)**
**Student:** Shahab Ali | ID: 503271 | Group: J4132
**Supervisor:** Professor Sergey Kovalchuk | 2025–2026

---

##Project Overview

Experimental implementation and quantitative benchmarking 
of multi-agent LLM roles within the OpenHands CodeAct 
framework. This study evaluates agent actions, observations, 
and memory structures to compare different role configurations 
across established software engineering benchmarks.

### Two Semester Journey:
- **Semester 1 (Theory):** Systematic Literature Review 
  following PRISMA guidelines. Analyzed 19 SOTA papers 
  (2023–2025) to build a 7-layer agent role taxonomy.
  
- **Semester 2 (Experiments):** Transitioned theory to 
  practice by benchmarking local vs cloud LLMs within 
  OpenHands to measure framework stability, role 
  effectiveness, and autonomous error recovery.

---

##  Agent Role Taxonomy (Semester 1)

Built from SLR of 19 state-of-the-art papers:

```
Agent Roles — 7 Layers
├── 1. Orchestration      → Manager, Supervisor
├── 2. Analysis/Planning  → Planner, PM
├── 3. Design             → Architect, Modeler
├── 4. Implementation     → Coder, Executor
├── 5. Quality Assurance  → Tester, Reviewer, Oracle
├── 6. Knowledge          → KG Curator, Writer
└── 7. Operations         → Tooling, Executor
```

**Key Trend Found:** QA layer dominates literature 
(9/19 papers) — shift from code generation to verification.

---

##  Methodology & Configurations

Two variables isolated:

**Variable 1 — LLM Scale:**
- Local 7B Parameter (Ollama — CodeLlama/Llama 3.1)
- Cloud 120B Parameter (Cerebras — gpt-oss-120b)

**Variable 2 — Agent Role Setup:**
- Setup A: Single Agent (Coder Only)
- Setup B: Multi-Agent Pair Programming (Coder + Tester)

**Benchmarks:**
- Phase 1: HumanEval (15 tasks)
- Phase 2: SWE-bench (6 tasks)

---

##  Phase 1: HumanEval Results (#1–15)

### By Configuration:

| # | LLM Scale | Agent Role | Tasks | Crash% | Self-Heal% | Pass% |
|---|-----------|------------|-------|--------|------------|-------|
| 1 | Local 7B | Single Coder | 5 |  100% | 0% | **0%** |
| 2 | Local 7B | Coder+Tester | 5 |  100% | 0% | **0%** |
| 3 | Cloud 120B | Single Coder | 5 | 0% |  100% |  **100%** |
| 4 | Cloud 120B | Coder+Tester | 10 | 0% |  100% |  **100%** |

### Complete Task Execution Matrix:

| Task | Config | LLM | Setup | Result | Error Type | Self-Healed |
|------|--------|-----|-------|--------|------------|-------------|
| #1 | 1 | 7B | A |  FAIL | Core Collapse | No |
| #2 | 3 | 120B | A |  FAIL | security_risk | No |
| #3 | 4 | 120B | B |  PASS | None | N/A |
| #4 | 3 | 120B | A |  PASS | None | N/A |
| #5 | 3 | 120B | A |  PASS | None | N/A |
| #6 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #7 | 3 | 120B | A |  PASS | security_risk |  Yes |
| #8 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #9 | 3 | 120B | A |  PASS | File Conflict |  Yes |
| #10 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #11 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #12 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #13 | 4 | 120B | B |  PASS | security_risk |  Yes |
| #14 | 4 | 120B | B |  PASS | Placeholder Hallucination |  Yes |
| #15 | 4 | 120B | B |  PASS | security_risk |  Yes |

---

## 📊 Phase 2: SWE-bench Results (#1–6)

| Task | Files | Anti-Paralysis | Result | Failure Type | Key Finding |
|------|-------|---------------|--------|--------------|-------------|
| SWE #1 | calculator+app |  No |  PASS | Token Limit | Agentic Loop |
| SWE #2 | app.py |  No |  FAIL | Missing Flask | Env Dependency |
| SWE #3 | calculator.py |  No |  FAIL | Verbose Paralysis | Chain Failure |
| SWE #4 | math_utils |  Yes |  PASS | None | Perfect 8/8 |
| SWE #5 | humaneval_results |  Yes |  PASS | None | Perfect 11/11 |
| SWE #6 | calculator ext. |  Yes |  PASS | Minor Paralysis | Recovered |

### Anti-Paralysis Prompt Impact:

| Condition | Tasks | Pass Rate |
|-----------|-------|-----------|
| Without Anti-Paralysis instruction | 3 |  33.3% |
| With Anti-Paralysis instruction | 3 |  100% |

> **Anti-Paralysis Instruction Used:**
> *"If any single action fails or repeats more than 3 times,
> STOP immediately. Run: ls /workspace/ to reorient yourself.
> Maximum 3 attempts per action."*

---

##  Key Discoveries

### 1. Framework Brittleness vs Cognitive Scale
Local 7B models: **100% crash rate** regardless of role.
Root cause: inability to follow strict XML tool-calling 
schemas in CodeAct architecture.
Cloud 120B models: **100% pass rate** on all HumanEval tasks.

### 2. Emergent Self-Healing Phenomenon 
The 120B model autonomously recovered from errors in 
**9/10 cases (90% recovery rate)**.
Types of errors self-healed:
- Missing `security_risk` XML parameter
- File conflict errors
- Placeholder hallucination (`...code...` literal text)
- Minor reasoning loops (5–6 attempts)

This capability was **completely absent** in 7B models.

### 3. Agentic Paralysis
Complex SWE-bench tasks induced reasoning loops where 
agent correctly identified next step but failed to execute.
- **Mild:** 5–6 repetitions before recovery
- **Severe (Verbose):** 200+ repetitions → Token exhaustion 
  → Chain failure cascade

### 4. Anti-Paralysis Prompt Engineering 
Single meta-cognitive constraint increased SWE-bench 
pass rate from **33.3% → 100%**.

### 5. Context Window Exhaustion
CI/CD terminal noise floods agent context window.
**Solutions developed:**
- Use `-q` flag on all pytest commands
- Use `head -n 20` to truncate outputs
- Pre-install all dependencies before agent execution
- Target specific test files (avoid cross-contamination)

---

##  Failure Taxonomy (10 Types Documented)

| # | Failure Type | Recovery | Prevention |
|---|-------------|----------|------------|
| 1 | XML Schema Error | Self-Heal | Partial |
| 2 | Context Collapse | None | Clear prompts |
| 3 | System Prompt Bleed | None | Simpler prompts |
| 4 | File Conflict | Pivot | N/A |
| 5 | Placeholder Hallucination | Self-Heal | Partial |
| 6 | Agentic Paralysis | None | Anti-Paralysis |
| 7 | Verbose Agentic Paralysis | Partial | Anti-Paralysis |
| 8 | Chain Failure | None | Anti-Paralysis |
| 9 | Environment Dependency | None | Pre-install deps |
| 10 | File Not Found | Exploration | Check workspace |

---

##  Overall Statistics

| Metric | Value |
|--------|-------|
| Total experimental runs | 21 |
| HumanEval tasks | 15 |
| SWE-bench tasks | 6 |
| Overall pass rate | **71.4%** |
| 7B model pass rate | **0%** |
| 120B model pass rate | **78.9%** |
| 120B HumanEval pass rate | **86.7%** |
| 120B SWE-bench pass rate | **66.7%** |
| Self-Healing success rate | **90%** |
| Failure types documented | **10** |
| New phenomena named | **4** |

---

##  Repository Structure

```
├── /experiments
│   ├── humaneval_0.py — humaneval_15.py
│   └── experiment_matrix.md
├── /implementation
│   ├── /workspace    → Solution files
│   ├── /tests        → Test files
│   └── /prompts      → Exact prompts used
├── /taxonomy         → Semester 1 SLR work
├── /docs             → Research paper + presentation
└── /reports          → Weekly progress reports
```

---

##  Replication Instructions

### 1. Start OpenHands Container:
```bash
export WORKSPACE_BASE=$(pwd)/workspace

docker run -it --rm --pull=always \
    -e SANDBOX_VOLUMES="$WORKSPACE_BASE:/workspace:rw" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -p 3000:3000 \
    --add-host host.docker.internal:host-gateway \
    ghcr.io/all-hands-ai/openhands:latest
```

### 2. Configure Model:
```
Open: http://localhost:3000
Settings → Model: cerebras/gpt-oss-120b
API Key: [your Cerebras API key]
```

### 3. Use Anti-Paralysis Prompt:
```
CRITICAL ANTI-PARALYSIS RULE:
If any single action fails or repeats more than
3 times → STOP immediately.
Run: ls /workspace/ to reorient.
Maximum 3 attempts per action.
```

### 4. Run Verification Tests:
```bash
python -m unittest test_calculator -q
python -m unittest test_math_utils -q
python -m unittest test_results_verify -q
```

---

##  Key Literature (Semester 1 SLR)

| Paper | Year | Key Role |
|-------|------|----------|
| MetaGPT | 2024 | PM, Architect, Engineer, QA |
| Magentic-One | 2025 | Manager, Specialist Agents |
| MapCoder | 2024 | Planner, Coder, Debugger |
| ChatDev | 2024 | CEO, CTO, Programmer, Reviewer |
| PotPie | 2025 | Debugger, Tester, KG Curator |

---

##  Contact

**Student:** Shahab Ali
**Student ID:** 503271
**Group:** J4132
**University:** ITMO University, Saint Petersburg
**Faculty:** FATII — Artificial Intelligence Technologies
**Supervisor:** Professor Sergey Kovalchuk
