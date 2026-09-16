#!/usr/bin/env python3
"""
Generate RESULTS_APPENDIX.md from the repository's experimental result files.

Phase 2 quantitative results are computed directly from the tracked result files.
Phase 1 observations are manually documented from qualitative weekly reports and
are explicitly labeled exploratory.

Run:
    python3 scripts/generate_appendix.py

Optional for the state-prediction section:
    data/HumanEval.jsonl

If data/HumanEval.jsonl is absent, the script also checks:
    ~/workspace/HumanEval.jsonl
"""

from pathlib import Path
import collections
import json
import re
import sys
from itertools import combinations

REPO = Path(__file__).resolve().parents[1]
EXP = REPO / "experiments"
OUT = REPO / "RESULTS_APPENDIX.md"

EVAL = EXP / "eval_results.jsonl"
SWE = EXP / "swe_results_FINAL.jsonl"
ABL = EXP / "ablation_results_FINAL.jsonl"
ABLSRC = EXP / "ablation_study.py"

TASK_CANDIDATES = [
    REPO / "data" / "HumanEval.jsonl",
    Path.home() / "workspace" / "HumanEval.jsonl",
]

CFGS = ["baseline", "coder", "coder_tester", "full_system"]
NICE = {
    "baseline": "Baseline",
    "coder": "Coder",
    "coder_tester": "Coder+Tester",
    "full_system": "Manager+Coder+Tester",
}


def load(path: Path):
    rows = []
    if not path.exists():
        print(f"  !! missing: {path}")
        return rows
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                print(f"  !! skipped malformed JSON line in {path.name}: {e}")
    return rows


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def hnum(t):
    m = re.search(r"(\d+)", str(t))
    return int(m.group(1)) if m else 0


he = load(EVAL)
swe = load(SWE)
abl = load(ABL)

task_file = first_existing(TASK_CANDIDATES)
tasks = {}
if task_file:
    tasks = {r["task_id"]: r for r in load(task_file)}
else:
    print("  !! HumanEval source file not found; state-prediction recomputation will be skipped.")

L = []
def w(s=""):
    L.append(s)


w("# Complete Experimental Appendix")
w()
w("Multi-Agent LLM Role Configurations for Software Engineering  ")
w("Shahab Ali · ITMO University · Student ID 503271 · Group J4132  ")
w("Supervisor: Prof. Sergey Kovalchuk")
w()
w("Phase 2 quantitative results below are computed directly from the tracked "
  "result files. Phase 1 observations are manually documented from qualitative "
  "weekly reports and are explicitly marked exploratory.")
w()
w("---")
w()

# A — RUN ACCOUNTING
w("## A. Run accounting")
w()

pairs = {(r["task_id"], r["config"]) for r in he}
dups = [
    p for p, c in collections.Counter(
        (r["task_id"], r["config"]) for r in he
    ).items() if c > 1
]

w("| Component | Design | Records |")
w("|---|---|---:|")
w(f"| HumanEval | 164 × 4 | {len(he)} |")
w(f"| SWE-bench Lite | 30 × 4 | {len(swe)} |")
w(f"| Prompt ablation | 20 × 7 | {len(abl)} |")
w(f"| **Phase 2 total** | | **{len(he)+len(swe)+len(abl)}** |")
w("| Phase 1 (exploratory; no structured event log) | manually documented | 21 |")
w(f"| **All-time total** | | **{len(he)+len(swe)+len(abl)+21}** |")
w()
w(f"Unique HumanEval task×config pairs: **{len(pairs)}**. "
  f"Duplicate records: **{len(dups)}**.")
w()

# B — HUMANEVAL
w("## B. HumanEval — 164 tasks, pass@1")
w()

stat = collections.defaultdict(lambda: {"p": 0, "f": 0, "e": collections.Counter()})
for r in he:
    c = r["config"]
    if r["passed"]:
        stat[c]["p"] += 1
    else:
        stat[c]["f"] += 1
        err = str(r.get("error") or "")
        for k in ("SyntaxError", "AssertionError", "NameError",
                  "TypeError", "IndexError", "ValueError"):
            if k in err:
                stat[c]["e"][k] += 1
                break
        else:
            stat[c]["e"]["EmptyCode/Other"] += 1

w("| Configuration | Pass | Fail | n | pass@1 |")
w("|---|---:|---:|---:|---:|")
for c in CFGS:
    s = stat[c]
    n = s["p"] + s["f"]
    if n:
        w(f"| {NICE[c]} | {s['p']} | {s['f']} | {n} | {s['p']/n*100:.1f}% |")
w()

w("**Failure breakdown**")
w()
kinds = sorted({k for c in CFGS for k in stat[c]["e"]})
w("| Configuration | " + " | ".join(kinds) + " |")
w("|---|" + "|".join(["---:"] * len(kinds)) + "|")
for c in CFGS:
    w(f"| {NICE[c]} | " +
      " | ".join(str(stat[c]["e"].get(k, 0)) for k in kinds) + " |")
w()

tc = collections.defaultdict(dict)
for r in he:
    tc[r["task_id"]][r["config"]] = bool(r["passed"])

decisive, rescued, lost, allfail = [], [], [], []
for t, d in tc.items():
    out = [d.get(c, False) for c in CFGS]
    if len(set(out)) > 1:
        decisive.append(t)
        if not d.get("baseline", False):
            rescued.append(t)
        else:
            lost.append(t)
    if not any(out):
        allfail.append(t)

w(f"**Architecture-sensitive tasks:** {len(decisive)} of {len(tc)} "
  f"(the other {len(tc)-len(decisive)} give identical outcomes).")
w()
w("| Task | " + " | ".join(NICE[c] for c in CFGS) + " | Category |")
w("|---|---|---|---|---|---|")
for t in sorted(decisive, key=hnum):
    d = tc[t]
    marks = " | ".join("PASS" if d.get(c) else "FAIL" for c in CFGS)
    cat = "rescued after baseline failure" if t in rescued else "lost by a role"
    w(f"| {t} | {marks} | {cat} |")
w()

w(f"Rescued after baseline failure: **{len(rescued)}** · "
  f"Lost by a role: **{len(lost)}**")
w()
w(f"**Solved by no configuration ({len(allfail)}):** " +
  ", ".join(sorted(allfail, key=hnum)))
w()
if tc:
    w(f"Maximum achievable task success across the observed configurations: "
      f"{len(tc)-len(allfail)}/{len(tc)} = "
      f"{(len(tc)-len(allfail))/len(tc)*100:.2f}%")
w()

# C — SWE-BENCH
w("## C. SWE-bench Lite — 30 repository tasks")
w()
w("Resolution uses **file-level diff overlap against the reference patch**, "
  "not the official SWE-bench test suite. Rates are comparable within this "
  "study only.")
w()

res = collections.defaultdict(dict)
times = collections.defaultdict(list)
for r in swe:
    tid = r.get("instance_id") or r.get("task_id")
    res[r["config"]][tid] = bool(r.get("resolved", False))
    if r.get("elapsed") is not None:
        times[r["config"]].append(float(r["elapsed"]))

w("| Configuration | Resolved | Failed | Rate | Mean runtime |")
w("|---|---:|---:|---:|---:|")
for c in CFGS:
    if c not in res:
        continue
    r_, n = sum(1 for v in res[c].values() if v), len(res[c])
    mt = sum(times[c]) / len(times[c]) if times[c] else 0
    w(f"| {NICE[c]} | {r_} | {n-r_} | {r_/n*100:.1f}% | {mt:.1f} s |")
w()

if times.get("coder") and times.get("coder_tester"):
    ov = (
        sum(times["coder_tester"]) / len(times["coder_tester"])
        - sum(times["coder"]) / len(times["coder"])
    )
    w(f"Observed mean runtime difference, Coder+Tester vs Coder: "
      f"**+{ov:.1f} s per task**.")
    w()

ids = sorted(res.get("baseline", {}))
w(f"**Task IDs ({len(ids)}), first-N slice of SWE-bench Lite**")
w()
w("| # | Instance | " + " | ".join(NICE[c] for c in CFGS) + " |")
w("|---:|---|---|---|---|---|")
for i, t in enumerate(ids, 1):
    w(f"| {i} | `{t}` | " +
      " | ".join("PASS" if res[c].get(t) else "FAIL" for c in CFGS) + " |")
w()

w("**Pairwise McNemar tests**")
w()
try:
    from scipy.stats import binomtest
    have_scipy = True
except ImportError:
    have_scipy = False

w("| Comparison | b01 | b10 | Discordant | p | Significant |")
w("|---|---:|---:|---:|---:|---|")
for a, b in combinations([c for c in CFGS if c in res], 2):
    sh = set(res[a]) & set(res[b])
    b01 = sum(1 for t in sh if not res[a][t] and res[b][t])
    b10 = sum(1 for t in sh if res[a][t] and not res[b][t])
    n = b01 + b10
    if have_scipy and n:
        p = binomtest(b01, n, 0.5).pvalue
        ps, sig = f"{p:.4f}", "yes" if p < 0.05 else "no"
    else:
        ps, sig = "n/a", "n/a"
    w(f"| {NICE[a]} vs {NICE[b]} | {b01} | {b10} | {n} | {ps} | {sig} |")
w()

# D — ABLATION
w("## D. Prompt ablation — 7 variants × 20 tasks")
w()
w("**Prompts, read verbatim from `experiments/ablation_study.py`**")
w()

if ABLSRC.exists():
    srctxt = ABLSRC.read_text(encoding="utf-8")
    blocks = re.findall(
        r'"(\w+)":\s*\{\s*"label":\s*"([^"]*)",\s*"prompt":\s*\((.*?)\)\s*\}',
        srctxt, re.S
    )
    for key, label, body in blocks:
        parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
        full = "".join(parts).replace("\\n", " ").replace("{task}", "").strip()
        w(f"- **{key}** — {label}  ")
        w(f"  `{full}`")
    w()
else:
    w("_source file not found; prompts not extracted_")
    w()

astat = collections.defaultdict(lambda: [0, 0])
for r in abl:
    astat[r["config"]][0 if r["passed"] else 1] += 1

w("| Variant | Pass | n | pass@1 |")
w("|---|---:|---:|---:|")
for k in ["baseline", "coder_A", "coder_B", "coder_C",
          "full_A", "full_B", "full_C"]:
    if k in astat:
        p, f = astat[k]
        w(f"| {k} | {p} | {p+f} | {p/(p+f)*100:.1f}% |")
w()

atasks = sorted({r["task_id"] for r in abl}, key=hnum)
w(f"Tasks used ({len(atasks)}): {', '.join(atasks)}")
w()
w("Variants were **not** token- or length-matched. The shortest constrained "
  "prompt passes 19/20 while the longest unconstrained prompt passes 0/20, "
  "making a length-only explanation unlikely without fully controlling for it.")
w()

# E — STATE PREDICTION
w("## E. State prediction (RQ1b)")
w()

FEATS = [
    "num_lines", "num_words", "num_chars", "return_hints", "uses_list",
    "uses_dict", "uses_optional", "docstring_blocks", "examples",
    "indentation", "complex_words", "type_count"
]

def feats(p):
    ws = p.split()
    return [
        len(p.strip().split("\n")),
        len(ws),
        len(p),
        p.count("->"),
        p.count("List"),
        p.count("Dict"),
        p.count("Optional"),
        p.count('"""'),
        p.count(">>>"),
        p.count("\n    "),
        len([x for x in ws if len(x) > 8]),
        p.count("int") + p.count("float") + p.count("str"),
    ]

if tasks:
    try:
        import numpy as np
        from sklearn.tree import DecisionTreeClassifier, export_text
        from sklearn.model_selection import cross_val_score, StratifiedKFold
        from sklearn.dummy import DummyClassifier

        X, y = [], []
        for t, d in tc.items():
            if t not in tasks:
                continue
            X.append(feats(tasks[t]["prompt"]))
            y.append(next((c for c in CFGS if d.get(c)), "baseline"))

        X, y = np.array(X), np.array(y)

        w("**Label rule:** first passing configuration in the fixed order "
          "baseline → coder → coder+tester → full system; tasks solved by no "
          "configuration default to baseline.")
        w()
        w("**Class distribution:** " +
          ", ".join(
              f"{k} {v}" for k, v in
              sorted(collections.Counter(y).items(), key=lambda x: -x[1])
          ))
        w()

        cv = StratifiedKFold(5, shuffle=True, random_state=42)
        dt = DecisionTreeClassifier(max_depth=4, random_state=42)
        sc = cross_val_score(dt, X, y, cv=cv)
        mj = cross_val_score(DummyClassifier(strategy="most_frequent"), X, y, cv=cv)

        w("| Policy | Classification accuracy |")
        w("|---|---:|")
        w(f"| Majority-class | {mj.mean()*100:.2f}% |")
        w(f"| Decision tree (depth 4, seed 42) | {sc.mean()*100:.2f}% |")
        w(f"| **Margin** | **{(sc.mean()-mj.mean())*100:+.2f} pp** |")
        w()
        w("Decision-tree fold scores: " + ", ".join(f"{s:.10f}" for s in sc))
        w()
        w("Majority-policy fold scores: " + ", ".join(f"{s:.10f}" for s in mj))
        w()

        dt.fit(X, y)
        w("**Feature importances**")
        w()
        w("| Feature | Importance |")
        w("|---|---:|")
        for f_, imp in sorted(zip(FEATS, dt.feature_importances_), key=lambda z: -z[1]):
            w(f"| {f_} | {imp:.6f} |")
        w()

        w("**Learned tree**")
        w()
        w("```text")
        w(export_text(dt, feature_names=FEATS).rstrip())
        w("```")
        w()

        nonbaseline = sum(1 for label in y if label != "baseline")
        w("The learned selector does not beat the trivial majority-class policy. "
          f"Under the first-success labeling rule, only **{nonbaseline} of {len(y)}** "
          "tasks receive a non-baseline label, producing severe class imbalance. "
          f"Separately, **{len(decisive)} of {len(tc)}** tasks are architecture-sensitive "
          "in the broader sense that at least one configuration changes the outcome. "
          "This is reported as a negative result.")
        w()

    except ImportError as e:
        w(f"_State-prediction recomputation skipped because a dependency is missing: {e}_")
        w()
else:
    w("_State-prediction recomputation skipped because HumanEval.jsonl was not found._")
    w()

# F — REPRODUCIBILITY
w("## F. Reproducibility record")
w()
w("| Item | Value |")
w("|---|---|")
for k, v in [
    ("Model", "claude-haiku-4-5 (Anthropic API), identical in all main configurations"),
    ("Framework", "OpenHands CodeAct in Docker"),
    ("Docker image", "`ghcr.io/all-hands-ai/openhands:latest` — **unpinned**"),
    ("HumanEval task selection", "all 164 tasks"),
    ("HumanEval timeout", "400 s per task"),
    ("HumanEval evaluation", "in-process exec + official `check()`"),
    ("SWE-bench Lite task selection", "first 30 tasks"),
    ("SWE-bench timeout", "600 s per task"),
    ("SWE-bench evaluation", "file-level git diff overlap vs reference patch"),
    ("Ablation task selection", "HumanEval/0–19"),
    ("Repeats", "single run per condition"),
    ("Temperature", "**not recorded**"),
    ("Random seed (generation)", "**not recorded**"),
    ("Selector seed", "random_state=42, 5-fold stratified CV"),
]:
    w(f"| {k} | {v} |")
w()
w("**Known limitations.** Single run per condition, so there is no variance "
  "estimate across repeated generations. Temperature and generation seed were "
  "not recorded, and the Docker image tag was unpinned. SWE-bench rates use an "
  "internal file-level criterion rather than the official test suite. The main "
  "evaluation uses one model family, and the ablation covers 20 tasks and one "
  "constraint type.")
w()

# G — PHASE 1
w("## G. Phase 1 (exploratory, 21 runs)")
w()
w("Phase 1 preceded the redesign and had no structured event logging. The "
  "following values are manually documented from qualitative weekly reports "
  "and are **not** controlled Phase 2 benchmark results.")
w()
w("- **Autonomous recovery:** 9 of 10 observed error events were followed by "
  "successful task completion without human intervention "
  "(`R_auto = 0.90`). Reconstructed from weekly reports.")
w("- **Agentic Paralysis:** the agent states the next action in reasoning but "
  "does not issue the corresponding tool call.")
w("- **Verbose paralysis case:** one run repeated similar reasoning 200+ times "
  "before a rate-limit / chain failure.")
w("- **Anti-paralysis instruction:** "
  "\"If any single action fails or repeats more than 3 times, STOP immediately. "
  "Run: ls /workspace/ to reorient yourself. Maximum 3 attempts per action.\" "
  "Observed 1/3 → 3/3 on six **different** tasks. This is a motivating "
  "observation, not a controlled causal comparison.")
w("- **Ten-type failure taxonomy:** catalogued qualitatively; types 1, 3 and 5 "
  "are candidate boundary-violation events for the proposed `V_boundary` metric.")
w()

OUT.write_text(
    "\n".join(line.rstrip() for line in L).rstrip() + "\n",
    encoding="utf-8"
)

print("=" * 68)
print("WROTE:", OUT)
print("=" * 68)
print(f"Runs        : HumanEval {len(he)} | SWE {len(swe)} | "
      f"Ablation {len(abl)} | +21 Phase 1 = {len(he)+len(swe)+len(abl)+21}")
for c in CFGS:
    s = stat[c]
    n = s["p"] + s["f"]
    if n:
        print(f"HumanEval   : {NICE[c]:<22} {s['p']}/{n} = {s['p']/n*100:.1f}%")
for c in CFGS:
    if c in res:
        r_, n = sum(1 for v in res[c].values() if v), len(res[c])
        print(f"SWE-bench   : {NICE[c]:<22} {r_}/{n} = {r_/n*100:.1f}%")
print(f"Sensitive   : {len(decisive)} tasks ({len(rescued)} rescued, {len(lost)} lost)")
print(f"All-fail    : {len(allfail)} -> {sorted(allfail, key=hnum)}")
print("=" * 68)
