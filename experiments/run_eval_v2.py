"""
Automated HumanEval Evaluation via OpenHands API
Shahab Ali - ITMO University - Group J4132
Supervisor: Professor Sergey Kovalchuk

Scientific Goal: Prove multi-agent role configurations
improve performance using the SAME model (gpt-oss-120b)

4 Configurations:
  Config 1: Baseline   - no roles
  Config 2: Coder      - single role
  Config 3: Coder+Tester - two roles
  Config 4: Manager+Coder+Tester - three roles
"""

import os
import re
import json
import time
import csv
import requests
import subprocess
from datetime import datetime

# ── Settings ─────────────────────────────────────────────────
OPENHANDS_URL = "http://localhost:3000"
DATASET_FILE  = "/home/shahab_ali/workspace/HumanEval.jsonl"
RESULTS_FILE  = "/home/shahab_ali/eval_results.jsonl"
CSV_FILE      = "/home/shahab_ali/eval_summary.csv"
MAX_WAIT      = 400   # seconds to wait for agent
CHECK_INTERVAL = 8    # seconds between checks
TASK_DELAY    = 3     # seconds between tasks

# ── Role Prompts ─────────────────────────────────────────────
CONFIGS = {
    "baseline": {
        "label": "Baseline (No Roles)",
        "prompt": (
            "Complete this Python function. "
            "Output ONLY the complete function code, "
            "no explanation, no markdown:\n\n{task}"
        )
    },
    "coder": {
        "label": "Coder Only",
        "prompt": (
            "You are a Coder agent. "
            "Your ONLY job is to write correct Python code. "
            "Output ONLY the complete function, no explanation:\n\n{task}"
        )
    },
    "coder_tester": {
        "label": "Coder + Tester",
        "prompt": (
            "You are a Pair Programming team:\n"
            "CODER: Write the Python function.\n"
            "TESTER: Check logic and fix any bugs.\n"
            "Output ONLY the final correct function:\n\n{task}"
        )
    },
    "full_system": {
        "label": "Manager + Coder + Tester",
        "prompt": (
            "You are a multi-agent system:\n"
            "MANAGER: Create a step-by-step logic plan.\n"
            "CODER: Implement the function from the plan.\n"
            "TESTER: Verify and fix any bugs.\n"
            "Output ONLY the final Python function:\n\n{task}"
        )
    },
}

# ── Load Dataset ─────────────────────────────────────────────
def load_dataset(path):
    tasks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    print(f"Loaded {len(tasks)} tasks")
    return tasks

# ── Extract Function from LLM Response ───────────────────────
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

# ── Test Solution ─────────────────────────────────────────────
def test_solution(code, canonical, test_code, entry_point):
    if not code or not code.strip():
        return {"passed": False, "error": "Empty code"}
    namespace = {}
    try:
        exec("from typing import List, Dict, Tuple, Optional, Any, Set", namespace)
        exec("from collections import defaultdict, Counter", namespace)
        exec("import math, re, string", namespace)
        exec(compile(code, "<generated>", "exec"), namespace)
        exec(compile(test_code, "<tests>", "exec"), namespace)
        if "check" in namespace and entry_point in namespace:
            namespace["check"](namespace[entry_point])
        elif entry_point not in namespace:
            return {"passed": False, "error": f"Function {entry_point} not found"}
        return {"passed": True, "error": None}
    except AssertionError as e:
        return {"passed": False, "error": f"AssertionError: {e}"}
    except SyntaxError as e:
        return {"passed": False, "error": f"SyntaxError: {e}"}
    except Exception as e:
        return {"passed": False, "error": f"{type(e).__name__}: {e}"}

# ── Extract Code from Events ──────────────────────────────────
def extract_code_from_events(events, entry_point):
    """Search all events for Python function code."""
    for event in reversed(events):
        source = event.get("source", "")
        if source != "agent":
            continue

        # Check message field
        msg = str(event.get("message", ""))
        if "def " in msg and len(msg) > 30:
            code = extract_function(msg, entry_point)
            if code:
                return code

        # Check content field
        cnt = str(event.get("content", ""))
        if "def " in cnt and len(cnt) > 30:
            code = extract_function(cnt, entry_point)
            if code:
                return code

        # Check args fields
        args = event.get("args", {})
        if isinstance(args, dict):
            for k, v in args.items():
                if isinstance(v, str) and "def " in v and len(v) > 30:
                    code = extract_function(v, entry_point)
                    if code:
                        return code

    return ""

# ── Send Task to OpenHands ────────────────────────────────────
def send_to_openhands(prompt, entry_point):
    """Send task to OpenHands and wait for code response."""

    # Create conversation
    try:
        resp = requests.post(
            f"{OPENHANDS_URL}/api/conversations",
            json={"initial_user_msg": prompt},
            timeout=30
        )
        if resp.status_code != 200:
            return ""
        conv_id = resp.json().get("conversation_id", "")
        if not conv_id:
            return ""
    except Exception as e:
        print(f"        Connection error: {e}")
        return ""

    # Poll for code in events
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
                code = extract_code_from_events(events, entry_point)
                if code:
                    return code
        except Exception as e:
            pass

    return ""

# ── Clean Runtime Containers ──────────────────────────────────
def cleanup_containers():
    subprocess.run(
        'docker rm $(docker ps -aq --filter "name=openhands-runtime" --filter "status=exited") 2>/dev/null || true',
        shell=True, capture_output=True
    )

# ── Load Completed Results ────────────────────────────────────
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

# ── Print Stats ───────────────────────────────────────────────
def print_stats(stats, done):
    print(f"\n--- Stats after {done} tasks ---")
    for cfg, s in stats.items():
        t = s["pass"] + s["fail"]
        pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<30}: {s['pass']:>3}/{t:<3} = {pct}%")
    print()

# ── Save CSV ──────────────────────────────────────────────────
def save_csv(stats):
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Configuration", "Pass", "Fail", "Total", "PassRate%"])
        for cfg, s in stats.items():
            t = s["pass"] + s["fail"]
            pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
            w.writerow([CONFIGS[cfg]["label"], s["pass"], s["fail"], t, pct])
    print(f"CSV saved: {CSV_FILE}")

# ── Main Evaluation ───────────────────────────────────────────
def run(num_tasks=10, start=0):
    print("\n" + "="*62)
    print("  AUTOMATED HUMANEVAL EVALUATION")
    print("  Shahab Ali - ITMO University - J4132")
    print(f"  Tasks: {num_tasks} | Start: {start}")
    print(f"  Model: claude-haiku-4-5 (SAME for ALL configs)")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62 + "\n")

    tasks = load_dataset(DATASET_FILE)
    tasks = tasks[start: start + num_tasks]

    # Warm up runtime before evaluation
    print("Warming up OpenHands runtime...")
    try:
        warmup_resp = requests.post(
            f"{OPENHANDS_URL}/api/conversations",
            json={"initial_user_msg": "print(hello)"},
            timeout=30
        )
        time.sleep(90)
        print("Warmup done!")
    except:
        print("Warmup skipped")

    completed, stats = load_completed()
    if completed:
        print(f"Resuming: {len(completed)} runs already done\n")

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
                print(f"  [{cfg['label']:<30}] SKIPPED")
                continue

            print(f"  [{cfg['label']:<30}] Running...", flush=True)
            t0 = time.time()

            try:
                full_prompt = cfg["prompt"].format(task=prompt)
                response = send_to_openhands(full_prompt, entry_pt)
                code = extract_function(response, entry_pt)
                result = test_solution(code, canonical, test_code, entry_pt)
                elapsed = round(time.time() - t0, 1)

                record = {
                    "task_id": task_id,
                    "config": cfg_name,
                    "label": cfg["label"],
                    "entry_point": entry_pt,
                    "passed": result["passed"],
                    "error": result["error"],
                    "elapsed": elapsed,
                    "code": code[:400],
                    "time": datetime.now().isoformat()
                }
                save_result(record)

                if result["passed"]:
                    stats[cfg_name]["pass"] += 1
                    print(f"  [{cfg['label']:<30}] PASS ({elapsed}s)")
                else:
                    stats[cfg_name]["fail"] += 1
                    err = (result["error"] or "")[:50]
                    print(f"  [{cfg['label']:<30}] FAIL ({elapsed}s) {err}")

            except Exception as e:
                stats[cfg_name]["fail"] += 1
                print(f"  [{cfg['label']:<30}] ERROR: {e}")
                save_result({
                    "task_id": task_id, "config": cfg_name,
                    "label": cfg["label"], "entry_point": entry_pt,
                    "passed": False, "error": str(e),
                    "elapsed": 0, "code": "",
                    "time": datetime.now().isoformat()
                })

            time.sleep(TASK_DELAY)

        # Clean up Docker containers after each task
        cleanup_containers()

        done = i + 1
        if done % 5 == 0:
            print_stats(stats, done)

    # Final report
    print("\n" + "="*62)
    print("  FINAL RESULTS")
    print("="*62)
    print(f"  {'Config':<30} {'Pass':>5} {'Fail':>5} {'Pass%':>7}")
    print(f"  {'-'*50}")
    for cfg, s in stats.items():
        t = s["pass"] + s["fail"]
        pct = round(s["pass"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<30} {s['pass']:>5} {s['fail']:>5} {pct:>6.1f}%")

    print(f"\n  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62)
    save_csv(stats)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", type=int, default=10)
    p.add_argument("--start", type=int, default=0)
    args = p.parse_args()
    run(args.tasks, args.start)
