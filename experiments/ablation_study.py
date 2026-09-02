"""
Prompt Ablation Study — Q1 Investigation
Shahab Ali - ITMO University - Group J4132
Supervisor: Professor Sergey Kovalchuk

Research Question 1:
"What details in the role prompt are most influencing?"

We test 3 variants of the Coder role prompt:
  Variant A: Identity only ("You are a Coder agent.")
  Variant B: Identity + Responsibility
  Variant C: Full prompt (what we already use)
  Baseline:  No role at all

Plus 3 variants for Manager+Coder+Tester:
  Variant D: Titles only
  Variant E: Titles + Responsibilities
  Variant F: Full prompts (what we already use)

Usage:
  python3 ablation_study.py --tasks 20
"""

import os
import re
import json
import time
import csv
import requests
from datetime import datetime

# ── Settings ─────────────────────────────────────────────────
OPENHANDS_URL  = "http://localhost:3000"
DATASET_FILE   = "/home/shahab_ali/workspace/HumanEval.jsonl"
RESULTS_FILE   = "/home/shahab_ali/ablation_results.jsonl"
CSV_FILE       = "/home/shahab_ali/ablation_summary.csv"
MAX_WAIT       = 400
CHECK_INTERVAL = 8
TASK_DELAY     = 3

# ── Prompt Variants ───────────────────────────────────────────
CONFIGS = {

    # ── Baseline ──────────────────────────────────────────────
    "baseline": {
        "label": "Baseline (No Role)",
        "prompt": (
            "Complete this Python function. "
            "Output ONLY the complete function code:\n\n{task}"
        )
    },

    # ── Coder Variants ────────────────────────────────────────
    "coder_A": {
        "label": "Coder A: Identity Only",
        "prompt": (
            "You are a Coder agent.\n\n{task}"
        )
    },

    "coder_B": {
        "label": "Coder B: Identity + Responsibility",
        "prompt": (
            "You are a Coder agent. "
            "Your ONLY job is to write correct Python code.\n\n{task}"
        )
    },

    "coder_C": {
        "label": "Coder C: Full Prompt",
        "prompt": (
            "You are a Coder agent. "
            "Your ONLY job is to write correct Python code. "
            "Output ONLY the complete function, "
            "no explanation, no markdown:\n\n{task}"
        )
    },

    # ── Full System Variants ──────────────────────────────────
    "full_A": {
        "label": "Full A: Titles Only",
        "prompt": (
            "You are a multi-agent system: "
            "MANAGER, CODER, TESTER.\n\n{task}"
        )
    },

    "full_B": {
        "label": "Full B: Titles + Responsibilities",
        "prompt": (
            "You are a multi-agent system:\n"
            "MANAGER: Plan the solution.\n"
            "CODER: Write the Python function.\n"
            "TESTER: Verify correctness.\n\n{task}"
        )
    },

    "full_C": {
        "label": "Full C: Full Prompt",
        "prompt": (
            "You are a multi-agent system:\n"
            "MANAGER: Create a step-by-step logic plan.\n"
            "CODER: Implement the function from the plan.\n"
            "TESTER: Verify and fix any bugs.\n"
            "Output ONLY the final Python function, "
            "no explanation, no markdown:\n\n{task}"
        )
    },
}

# ── Helper: Extract Function ──────────────────────────────────
def extract_function(text, entry_point):
    if not text:
        return ""
    text = re.sub(r"```python\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()
    lines = text.split("\n")
    func_lines = []
    inside = False
    for line in lines:
        if f"def {entry_point}" in line:
            inside = True
        if inside:
            if (func_lines and line.strip() and
                    not line.startswith(" ") and
                    not line.startswith("\t") and
                    line.strip().startswith("def ") and
                    f"def {entry_point}" not in line):
                break
            func_lines.append(line)
    return "\n".join(func_lines) if func_lines else text

# ── Helper: Test Solution ─────────────────────────────────────
def test_solution(code, canonical, test_code, entry_point):
    if not code or not code.strip():
        return {"passed": False, "error": "Empty code"}
    namespace = {}
    try:
        exec("from typing import List, Dict, Tuple, Optional, Any, Set",
             namespace)
        exec("from collections import defaultdict, Counter", namespace)
        exec("import math, re, string", namespace)
        exec(compile(code, "<generated>", "exec"), namespace)
        exec(compile(test_code, "<tests>", "exec"), namespace)
        if "check" in namespace and entry_point in namespace:
            namespace["check"](namespace[entry_point])
        elif entry_point not in namespace:
            return {"passed": False,
                    "error": f"Function {entry_point} not found"}
        return {"passed": True, "error": None}
    except AssertionError as e:
        return {"passed": False, "error": f"AssertionError: {e}"}
    except SyntaxError as e:
        return {"passed": False, "error": f"SyntaxError: {e}"}
    except Exception as e:
        return {"passed": False, "error": f"{type(e).__name__}: {e}"}

# ── Send to OpenHands ─────────────────────────────────────────
def send_to_openhands(prompt, entry_point):
    try:
        resp = requests.post(
            f"{OPENHANDS_URL}/api/conversations",
            json={"initial_user_msg": prompt},
            timeout=60
        )
        if resp.status_code != 200:
            return ""
        conv_id = resp.json().get("conversation_id", "")
        if not conv_id:
            return ""
    except Exception as e:
        print(f"        Connection error: {e}")
        return ""

    waited = 0
    while waited < MAX_WAIT:
        time.sleep(CHECK_INTERVAL)
        waited += CHECK_INTERVAL
        try:
            er = requests.get(
                f"{OPENHANDS_URL}/api/conversations/{conv_id}/events",
                timeout=15
            )
            if er.status_code == 200:
                events = er.json().get("events", [])
                for event in reversed(events):
                    if event.get("source") == "agent":
                        msg = str(event.get("message", ""))
                        cnt = str(event.get("content", ""))
                        args = event.get("args", {})
                        if isinstance(args, dict):
                            for v in args.values():
                                if (isinstance(v, str) and
                                        "def " in v and len(v) > 30 and
                                        "OpenHands agent" not in v):
                                    return v
                        text = msg if len(msg) > len(cnt) else cnt
                        if (text and "def " in text and
                                len(text) > 30 and
                                "OpenHands agent" not in text):
                            return text
        except Exception:
            pass
    return ""

# ── Load Dataset ──────────────────────────────────────────────
def load_dataset(path, num=20):
    tasks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks[:num]

# ── Load Completed ────────────────────────────────────────────
def load_completed():
    completed = set()
    stats = {cfg: {"pass": 0, "fail": 0} for cfg in CONFIGS}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            for line in f:
                try:
                    r = json.loads(line.strip())
                    completed.add((r["task_id"], r["config"]))
                    cfg = r["config"]
                    if cfg in stats:
                        if r["passed"]:
                            stats[cfg]["pass"] += 1
                        else:
                            stats[cfg]["fail"] += 1
                except:
                    pass
    return completed, stats

# ── Save Result ───────────────────────────────────────────────
def save_result(record):
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

# ── Save CSV ──────────────────────────────────────────────────
def save_csv(stats):
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Config", "Label", "Pass", "Fail", "Total", "PassRate%"])
        for cfg, s in stats.items():
            t = s["pass"] + s["fail"]
            pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
            w.writerow([cfg, CONFIGS[cfg]["label"],
                        s["pass"], s["fail"], t, pct])
    print(f"CSV saved: {CSV_FILE}")

# ── Print Stats ───────────────────────────────────────────────
def print_stats(stats, done):
    print(f"\n--- Ablation Stats after {done} tasks ---")
    print(f"{'Config':<35} {'Pass':>5} {'Fail':>5} {'Pass%':>7}")
    print("-"*55)
    for cfg, s in stats.items():
        t = s["pass"] + s["fail"]
        pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<33} {s['pass']:>5} "
              f"{s['fail']:>5} {pct:>6.1f}%")
    print()

# ── Main ──────────────────────────────────────────────────────
def run(num_tasks=20):
    print("\n" + "="*62)
    print("  PROMPT ABLATION STUDY — Q1 INVESTIGATION")
    print("  Shahab Ali - ITMO University - J4132")
    print(f"  Tasks: {num_tasks}")
    print(f"  Question: Which prompt component matters most?")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62 + "\n")

    print("Prompt Variants Being Tested:")
    for cfg, c in CONFIGS.items():
        print(f"  {cfg:<12}: {c['label']}")
    print()

    tasks = load_dataset(DATASET_FILE, num_tasks)
    print(f"Loaded {len(tasks)} tasks\n")

    completed, stats = load_completed()
    if completed:
        print(f"Resuming: {len(completed)} runs done\n")

    for i, task in enumerate(tasks):
        task_id   = task["task_id"]
        prompt    = task["prompt"]
        entry_pt  = task["entry_point"]
        test_code = task["test"]
        canonical = task["canonical_solution"]

        print(f"\n{'='*62}")
        print(f"Task [{i+1}/{len(tasks)}]: {task_id} ({entry_pt})")
        print("="*62)

        for cfg_name, cfg in CONFIGS.items():
            if (task_id, cfg_name) in completed:
                print(f"  [{cfg['label']:<33}] SKIPPED")
                continue

            print(f"  [{cfg['label']:<33}] Running...", flush=True)
            t0 = time.time()

            try:
                full_prompt = cfg["prompt"].format(task=prompt)
                response = send_to_openhands(full_prompt, entry_pt)
                code = extract_function(response, entry_pt)
                result = test_solution(code, canonical,
                                       test_code, entry_pt)
                elapsed = round(time.time() - t0, 1)

                record = {
                    "task_id":    task_id,
                    "config":     cfg_name,
                    "label":      cfg["label"],
                    "entry_point": entry_pt,
                    "passed":     result["passed"],
                    "error":      result["error"],
                    "elapsed":    elapsed,
                    "code":       code[:300],
                    "time":       datetime.now().isoformat()
                }
                save_result(record)

                if result["passed"]:
                    stats[cfg_name]["pass"] += 1
                    print(f"  [{cfg['label']:<33}] "
                          f"PASS ({elapsed}s)")
                else:
                    stats[cfg_name]["fail"] += 1
                    err = (result["error"] or "")[:40]
                    print(f"  [{cfg['label']:<33}] "
                          f"FAIL ({elapsed}s) {err}")

            except Exception as e:
                stats[cfg_name]["fail"] += 1
                print(f"  [{cfg['label']:<33}] ERROR: {e}")
                save_result({
                    "task_id": task_id, "config": cfg_name,
                    "label": cfg["label"],
                    "entry_point": entry_pt,
                    "passed": False, "error": str(e),
                    "elapsed": 0, "code": "",
                    "time": datetime.now().isoformat()
                })

            time.sleep(TASK_DELAY)

        done = i + 1
        if done % 5 == 0:
            print_stats(stats, done)

    # Final report
    print("\n" + "="*62)
    print("  ABLATION STUDY FINAL RESULTS")
    print("="*62)
    print(f"\n  {'Config':<35} {'Pass':>5} {'Fail':>5} {'Pass%':>7}")
    print(f"  {'-'*55}")

    print("\n  --- Baseline vs Coder Variants ---")
    for cfg in ["baseline", "coder_A", "coder_B", "coder_C"]:
        s = stats[cfg]
        t = s["pass"] + s["fail"]
        pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<35} "
              f"{s['pass']:>5} {s['fail']:>5} {pct:>6.1f}%")

    print("\n  --- Full System Variants ---")
    for cfg in ["full_A", "full_B", "full_C"]:
        s = stats[cfg]
        t = s["pass"] + s["fail"]
        pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<35} "
              f"{s['pass']:>5} {s['fail']:>5} {pct:>6.1f}%")

    print(f"\n  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62)
    save_csv(stats)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", type=int, default=20)
    args = p.parse_args()
    run(args.tasks)
