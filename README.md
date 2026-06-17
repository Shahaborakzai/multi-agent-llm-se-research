# 🤖 Multi-Agent LLM Evaluation for Software Engineering

**ITMO University | Faculty of AI Technologies (FATII)**  
**Program:** Big Data and Machine Learning  
**Student:** Shahab Ali | ID: 503271 | Group: J4132  
**Supervisor:** Professor Sergey Kovalchuk  
**Year:** 2025–2026  

---

## 📋 Project Overview

This research project investigates how different 
Large Language Model (LLM) configurations and 
agent role assignments affect performance on 
software engineering benchmarks using the 
OpenHands CodeAct framework.

### Research Questions:
- **RQ1:** What are the key agentic roles in 
  LLM-based software engineering frameworks?
- **RQ2:** How are these roles technically 
  represented in LLM context?

---

## 🏗️ Agent Role Taxonomy

Built from Systematic Literature Review of 
19 state-of-the-art papers (2023–2025):

```
Agent Roles (7 Layers)
├── 1. Orchestration → Manager, Supervisor
├── 2. Analysis & Planning → Planner, PM
├── 3. Design → Architect, Modeler
├── 4. Implementation → Coder, Executor
├── 5. Quality Assurance → Tester, Reviewer
├── 6. Knowledge → KG Curator, Writer
└── 7. Operations → Tooling, Executor
```

---

## ⚙️ Experimental Setup

| Component | Detail |
|-----------|--------|
| Framework | OpenHands CodeAct |
| Container | Docker + Ubuntu/WSL |
| Cloud API | Cerebras (gpt-oss-120b) |
| Local Model | Ollama (Llama 3.1 — 7B) |
| Benchmarks | HumanEval + SWE-bench |
| Total Runs | 21 experiments |

### 4 Configurations Tested:

| Config | LLM | Role |
|--------|-----|------|
| 1 | Local 7B | Single Agent (Coder) |
| 2 | Local 7B | Multi Agent (Coder+Tester) |
| 3 | Cloud 120B | Single Agent (Coder) |
| 4 | Cloud 120B | Multi Agent (Coder+Tester) |

---

## 📊 Key Results

### HumanEval (#1–15):

| Config | LLM | Role | Tasks | Pass% | Crash% |
|--------|-----|------|-------|-------|--------|
| 1 | 7B | Single Coder | 5 | 0% | 100% |
| 2 | 7B | Coder+Tester | 5 | 0% | 100% |
| 3 | 120B | Single Coder | 5 | 100% | 0% |
| 4 | 120B | Coder+Tester | 10 | 100% | 0% |

### SWE-bench (#1–6):

| Task | Anti-Paralysis | Result |
|------|---------------|--------|
| SWE #1 | No | ✅ PASS |
| SWE #2 | No | ❌ FAIL |
| SWE #3 | No | ❌ FAIL |
| SWE #4 | Yes | ✅ PASS |
| SWE #5 | Yes | ✅ PASS |
| SWE #6 | Yes | ✅ PASS |

### Anti-Paralysis Impact:
| Condition | Pass Rate |
|-----------|-----------|
| Without instruction | 33.3% |
| With instruction | 100% |

---

## 🔬 Key Findings

**1. Framework Brittleness vs Scale**
- 7B models: 100% crash rate
- 120B models: 100% pass rate
- Scale is PRIMARY success factor

**2. Self-Healing Phenomenon**
- 120B model auto-corrected 9/10 errors
- 90% recovery rate
- Absent in 7B models completely

**3. Agentic Paralysis**
- Complex tasks cause reasoning loops
- Severe case: 200+ loops → crash
- New failure type documented

**4. Anti-Paralysis Prompt Engineering**
- Single instruction: 33.3% → 100% pass rate
- Practical solution for agentic failures

**5. Context Window Exhaustion**
- CI/CD noise floods context window
- Solution: -q flag + head -n 20

---

## 🗂️ Failure Taxonomy (10 Types)

| # | Type | Recovery |
|---|------|----------|
| 1 | XML Schema Error | Self-Healed |
| 2 | Context Collapse | None |
| 3 | System Prompt Bleed | None |
| 4 | File Conflict | Pivot |
| 5 | Placeholder Hallucination | Self-Healed |
| 6 | Agentic Paralysis | None |
| 7 | Verbose Agentic Paralysis | Partial |
| 8 | Chain Failure | None |
| 9 | Environment Dependency | None |
| 10 | File Not Found | Exploration |

---

## 📁 Repository Structure

```
├── /docs            → Research paper + presentation
├── /experiments     → All experimental results
├── /implementation  → Source code + test files
│   ├── /workspace   → Python solutions
│   ├── /tests       → Test files
│   └── /prompts     → Exact prompts used
├── /taxonomy        → Agent role taxonomy
└── /reports         → Progress reports
```

---

## 🚀 How to Reproduce

### 1. Install Docker:
```bash
sudo apt-get install docker.io
```

### 2. Run OpenHands:
```bash
export WORKSPACE_BASE=$(pwd)/workspace

docker run -it --rm --pull=always \
-e SANDBOX_VOLUMES="$WORKSPACE_BASE:/workspace:rw" \
-v /var/run/docker.sock:/var/run/docker.sock \
-p 3000:3000 \
--add-host host.docker.internal:host-gateway \
ghcr.io/all-hands-ai/openhands:latest
```

### 3. Configure in OpenHands UI:
```
Go to: http://localhost:3000
Settings → Model: cerebras/gpt-oss-120b
API Key: [your Cerebras API key]
```

### 4. Run Tests:
```bash
python -m unittest test_calculator -q
python -m unittest test_math_utils -q
```

---

## 📈 Summary Statistics

| Metric | Value |
|--------|-------|
| Total runs | 21 |
| Overall pass rate | 71.4% |
| 7B model pass rate | 0% |
| 120B model pass rate | 78.9% |
| Self-Healing success rate | 90% |
| Failure types documented | 10 |
| New phenomena named | 4 |

---

## 👤 Contact

**Student:** Shahab Ali  
**Student ID:** 503271  
**Group:** J4132  
**University:** ITMO University, Saint Petersburg  
**Supervisor:** Professor Sergey Kovalchuk
