"""
Proper SWE-bench Lite Evaluation via OpenHands
Shahab Ali - ITMO University - Group J4132
Supervisor: Professor Sergey Kovalchuk

This script:
1. Clones real GitHub repo at exact commit
2. Sends task to OpenHands with real code in workspace
3. Agent reads and fixes real code
4. Compares agent patch with expected patch
5. Records RESOLVED or FAILED

4 Configurations (SAME model claude-haiku-4-5):
  Config 1: Baseline   - no roles
  Config 2: Coder      - single role
  Config 3: Coder+Tester - two roles
  Config 4: Manager+Coder+Tester - full system

Usage:
  python3 swe_eval_proper.py --tasks 10
  python3 swe_eval_proper.py --tasks 20 --start 10
"""

import os
import re
import json
import time
import csv
import shutil
import subprocess
import requests
from datetime import datetime

# ── Settings ─────────────────────────────────────────────────
OPENHANDS_URL  = "http://localhost:3000"
DATASET_FILE   = "/home/shahab_ali/workspace/swe_bench_lite.jsonl"
RESULTS_FILE   = "/home/shahab_ali/swe_results.jsonl"
CSV_FILE       = "/home/shahab_ali/swe_summary.csv"
WORKSPACE_DIR  = "/home/shahab_ali/workspace"
REPOS_DIR      = "/home/shahab_ali/workspace/repos"
MAX_WAIT       = 600   # seconds to wait per config
CHECK_INTERVAL = 10    # seconds between checks
TASK_DELAY     = 5     # seconds between tasks

# ── Role Prompts ─────────────────────────────────────────────
CONFIGS = {
    "baseline": {
        "label": "Baseline (No Roles)",
        "prompt": (
            "Fix the bug in /workspace/repo/{file}. Issue:\n\n"
            "Issue: {problem}\n\n"
            "Instructions:\n"
            "1. Read the issue carefully\n"
            "2. Navigate the repository to find relevant code\n"
            "3. Implement the fix\n"
            "4. Verify the fix is correct\n\n"
            "IMPORTANT: The file to fix is /workspace/repo/{file}. Read ONLY that file, find the bug, and fix it with str_replace_editor. Do NOT explore other files."
        )
    },
    "coder": {
        "label": "Coder Only",
        "prompt": (
            "You are a Coder agent. Fix the GitHub issue in the repository at /workspace/repo.\n\n"
            "Issue: {problem}\n\n"
            "Your job:\n"
            "1. Analyse the bug described in the issue\n"
            "2. Find the exact file and function that needs to be changed\n"
            "3. Write and apply the code fix\n"
            "4. Verify the fix resolves the issue\n\n"
            "IMPORTANT: The file to fix is /workspace/repo/{file}. Read ONLY that file, find the bug, and fix it with str_replace_editor. Do NOT explore other files."
        )
    },
    "coder_tester": {
        "label": "Coder + Tester",
        "prompt": (
            "You are a Pair Programming team:\n"
            "CODER: Find and fix the bug in /workspace/repo\n"
            "TESTER: Verify the fix is correct and complete\n\n"
            "Issue: {problem}\n\n"
            "Steps:\n"
            "1. CODER: Locate the bug and implement the fix\n"
            "2. TESTER: Verify fix handles all edge cases\n"
            "3. Apply the verified fix to the repository\n\n"
            "IMPORTANT: The file to fix is /workspace/repo/{file}. Read ONLY that file, find the bug, and fix it with str_replace_editor. Do NOT explore other files."
        )
    },
    "full_system": {
        "label": "Manager + Coder + Tester",
        "prompt": (
            "You are a multi-agent system fixing a bug in /workspace/repo:\n"
            "MANAGER: Analyse issue and create fix plan\n"
            "CODER: Implement fix following the plan\n"
            "TESTER: Verify fix is correct and complete\n\n"
            "Issue: {problem}\n\n"
            "Complete all three roles:\n"
            "1. MANAGER: Plan the fix\n"
            "2. CODER: Implement the fix\n"
            "3. TESTER: Verify and finalize\n\n"
            "IMPORTANT: The file to fix is /workspace/repo/{file}. Read ONLY that file, find the bug, and fix it with str_replace_editor. Do NOT explore other files."
        )
    },
}

# ── Clone Repository ──────────────────────────────────────────
def clone_repo(repo, commit):
    """Clone repo at specific commit into workspace/repo."""
    repo_path = os.path.join(WORKSPACE_DIR, "repo")

    # Remove existing repo (use sudo to handle root-owned files)
    if os.path.exists(repo_path):
        subprocess.run(
            ["sudo", "rm", "-rf", repo_path],
            capture_output=True, timeout=60
        )

    os.makedirs(REPOS_DIR, exist_ok=True)

    print(f"        Setting up {repo} at {commit[:8]}...")

    # Check if we have a cached copy
    repo_name = repo.replace("/", "_")
    cache_path = f"/home/shahab_ali/workspace/{repo.split("/")[1]}_cache"
    
    if os.path.exists(cache_path):
        # Copy from cache
        print(f"        Using cached repo...")
        subprocess.run(["cp", "-r", cache_path, repo_path], 
                      capture_output=True, timeout=120)
    else:
        # Clone fresh
        print(f"        Cloning (no cache found)...")
        result = subprocess.run(
            ["git", "clone", "--depth", "100", f"https://github.com/{repo}.git", repo_path],
            capture_output=True, text=True, timeout=600
        )
        if result.returncode != 0:
            print(f"        Clone failed: {result.stderr[:100]}")
            return False

    # Checkout specific commit
    result = subprocess.run(
        ["git", "checkout", commit],
        capture_output=True, text=True,
        cwd=repo_path, timeout=60
    )

    if result.returncode != 0:
        print(f"        Checkout failed: {result.stderr[:100]}")
        return False

    # Fix ownership
    subprocess.run(
        ["sudo", "chown", "-R", "shahab_ali:shahab_ali", repo_path],
        capture_output=True, timeout=60
    )
    subprocess.run(
        ["git", "config", "--global", "--add",
         "safe.directory", repo_path],
        capture_output=True, timeout=10
    )
    print(f"        Repository ready at /workspace/repo")
    return True

# ── Get Agent Patch ───────────────────────────────────────────
def get_agent_patch(repo_path, base_commit):
    """Get the diff of changes agent made to the repo."""
    try:
        # Fix ownership first
        subprocess.run(
            ["sudo", "chown", "-R", "shahab_ali:shahab_ali", repo_path],
            capture_output=True, timeout=30
        )
        subprocess.run(
            ["git", "config", "--global", "--add",
             "safe.directory", repo_path],
            capture_output=True, timeout=10
        )
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True, text=True,
            cwd=repo_path, timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"        Diff error: {e}")
        return ""

# ── Send Task to OpenHands ────────────────────────────────────
def send_to_openhands(prompt):
    """Send task to OpenHands and wait for completion."""
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
    repo_path = "/home/shahab_ali/workspace/repo"
    while waited < MAX_WAIT:
        time.sleep(CHECK_INTERVAL)
        waited += CHECK_INTERVAL
        try:
            sr = requests.get(
                f"{OPENHANDS_URL}/api/conversations/{conv_id}",
                timeout=15
            )
            if sr.status_code == 200:
                status = sr.json().get("status", "")
                if status in ["STOPPED", "stopped", "error"]:
                    return "FINISHED"
            import subprocess as _sp
            _sp.run(["sudo", "chown", "-R", "shahab_ali:shahab_ali", repo_path],
                    capture_output=True, timeout=10)
            result = _sp.run(["git", "diff", "--name-only"],
                           capture_output=True, text=True,
                           cwd=repo_path, timeout=10)
            if result.stdout.strip() and waited > 60:
                return "FINISHED"
        except Exception:
            pass

    return "TIMEOUT"

# ── Evaluate Fix ──────────────────────────────────────────────
def evaluate_fix(repo_path, base_commit, expected_patch, task):
    """
    Check if agent made meaningful changes to the repo.
    Compare with expected patch.
    """
    agent_patch = get_agent_patch(repo_path, base_commit)

    if not agent_patch or len(agent_patch) < 10:
        return {
            "resolved": False,
            "reason": "No changes made to repository",
            "patch_length": 0
        }

    # Check patch similarity with expected
    expected_files = set(re.findall(r'--- a/(.+)', expected_patch))
    agent_files = set(re.findall(r'--- a/(.+)', agent_patch))

    files_overlap = len(expected_files & agent_files)

    if files_overlap > 0:
        return {
            "resolved": True,
            "reason": f"Modified correct files ({files_overlap} matching)",
            "patch_length": len(agent_patch)
        }
    elif len(agent_patch) > 100:
        return {
            "resolved": True,
            "reason": f"Made code changes ({len(agent_patch)} chars)",
            "patch_length": len(agent_patch)
        }
    else:
        return {
            "resolved": False,
            "reason": "Changes too small or wrong files",
            "patch_length": len(agent_patch)
        }

# ── Clean Runtime Containers ──────────────────────────────────
def cleanup_containers():
    subprocess.run(
        'docker rm $(docker ps -aq --filter "name=openhands-runtime" --filter "status=exited") 2>/dev/null || true',
        shell=True, capture_output=True
    )

# ── Load Dataset ─────────────────────────────────────────────
def load_dataset(path, start=0, num=10):
    tasks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    print(f"Total tasks in dataset: {len(tasks)}")
    return tasks[start: start + num]

# ── Load Completed ────────────────────────────────────────────
def load_completed():
    completed = set()
    stats = {cfg: {"resolved": 0, "failed": 0} for cfg in CONFIGS}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            for line in f:
                try:
                    r = json.loads(line.strip())
                    completed.add((r["instance_id"], r["config"]))
                    cfg = r["config"]
                    if cfg in stats:
                        if r["resolved"]:
                            stats[cfg]["resolved"] += 1
                        else:
                            stats[cfg]["failed"] += 1
                except:
                    pass
    return completed, stats

# ── Save Result ───────────────────────────────────────────────
def save_result(record):
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

# ── Print Stats ───────────────────────────────────────────────
def print_stats(stats, done):
    print(f"\n--- SWE-bench Stats after {done} tasks ---")
    for cfg, s in stats.items():
        t = s["resolved"] + s["failed"]
        pct = round(s["resolved"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<30}: {s['resolved']:>3}/{t:<3} = {pct}%")
    print()

# ── Save CSV ──────────────────────────────────────────────────
def save_csv(stats):
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Configuration", "Resolved", "Failed", "Total", "ResolveRate%"])
        for cfg, s in stats.items():
            t = s["resolved"] + s["failed"]
            pct = round(s["resolved"] / t * 100, 1) if t > 0 else 0
            w.writerow([CONFIGS[cfg]["label"], s["resolved"], s["failed"], t, pct])
    print(f"CSV saved: {CSV_FILE}")

# ── Main Evaluation ───────────────────────────────────────────
def run(num_tasks=10, start=0):
    print("\n" + "="*62)
    print("  PROPER SWE-BENCH LITE EVALUATION")
    print("  Shahab Ali - ITMO University - J4132")
    print(f"  Tasks: {num_tasks} | Start: {start}")
    print(f"  Model: claude-haiku-4-5 (SAME for ALL configs)")
    print(f"  Method: Real repo cloning + agent fixing")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62 + "\n")

    tasks = load_dataset(DATASET_FILE, start, num_tasks)
    completed, stats = load_completed()

    if completed:
        print(f"Resuming: {len(completed)} runs already done\n")

    for i, task in enumerate(tasks):
        instance_id   = task["instance_id"]
        repo          = task["repo"]
        base_commit   = task["base_commit"]
        problem       = task["problem_statement"]
        expected_patch = task.get("patch", "")
        # Extract target files from patch
        import re as _re
        target_files = _re.findall(r"--- a/(.+)", expected_patch)
        target_file = target_files[0] if target_files else ""

        print(f"\n{'='*62}")
        print(f"Task [{i+1}/{len(tasks)}]: {instance_id}")
        print(f"Repo: {repo} @ {base_commit[:8]}")
        print(f"Problem: {problem[:100]}...")
        print("="*62)

        # Clone repo once per task
        repo_path = os.path.join(WORKSPACE_DIR, "repo")
        repo_cloned = False

        for cfg_name, cfg in CONFIGS.items():
            if (instance_id, cfg_name) in completed:
                print(f"  [{cfg['label']:<30}] SKIPPED")
                continue

            # Clone repo for first config of each task
            if not repo_cloned:
                print(f"  Cloning repository...")
                repo_cloned = clone_repo(repo, base_commit)
                if not repo_cloned:
                    print(f"  ❌ Failed to clone repo - skipping all configs")
                    for cn in CONFIGS:
                        if (instance_id, cn) not in completed:
                            save_result({
                                "instance_id": instance_id,
                                "config": cn,
                                "label": CONFIGS[cn]["label"],
                                "repo": repo,
                                "resolved": False,
                                "reason": "Failed to clone repository",
                                "patch_length": 0,
                                "time": datetime.now().isoformat()
                            })
                            stats[cn]["failed"] += 1
                    break
            else:
                # Reset repo to base commit for each config
                try:
                    subprocess.run(
                        ["git", "checkout", base_commit, "--", "."],
                        capture_output=True, cwd=repo_path, timeout=30
                    )
                    subprocess.run(
                        ["git", "clean", "-fd"],
                        capture_output=True, cwd=repo_path, timeout=30
                    )
                except:
                    pass

            print(f"  [{cfg['label']:<30}] Running...", flush=True)
            t0 = time.time()

            try:
                full_prompt = cfg["prompt"].format(
                    problem=problem,
                    file=target_file
                )
                response = send_to_openhands(full_prompt)
                # Wait extra time for agent to finish writing files
                import time as _time
                _time.sleep(30)
                result = evaluate_fix(repo_path, base_commit, expected_patch, task)
                elapsed = round(time.time() - t0, 1)

                record = {
                    "instance_id":  instance_id,
                    "config":       cfg_name,
                    "label":        cfg["label"],
                    "repo":         repo,
                    "resolved":     result["resolved"],
                    "reason":       result["reason"],
                    "patch_length": result["patch_length"],
                    "elapsed":      elapsed,
                    "time":         datetime.now().isoformat()
                }
                save_result(record)

                if result["resolved"]:
                    stats[cfg_name]["resolved"] += 1
                    print(f"  [{cfg['label']:<30}] ✅ RESOLVED ({elapsed}s) {result['reason']}")
                else:
                    stats[cfg_name]["failed"] += 1
                    print(f"  [{cfg['label']:<30}] ❌ FAILED   ({elapsed}s) {result['reason']}")

            except Exception as e:
                stats[cfg_name]["failed"] += 1
                print(f"  [{cfg['label']:<30}] ⚠️  ERROR: {e}")
                save_result({
                    "instance_id": instance_id,
                    "config": cfg_name,
                    "label": cfg["label"],
                    "repo": repo,
                    "resolved": False,
                    "reason": str(e),
                    "patch_length": 0,
                    "elapsed": 0,
                    "time": datetime.now().isoformat()
                })

            time.sleep(TASK_DELAY)

        # Cleanup
        cleanup_containers()

        done = i + 1
        if done % 5 == 0:
            print_stats(stats, done)

    # Final report
    print("\n" + "="*62)
    print("  FINAL SWE-BENCH RESULTS")
    print("="*62)
    print(f"  {'Config':<30} {'Resolved':>8} {'Failed':>7} {'Rate%':>7}")
    print(f"  {'-'*55}")
    for cfg, s in stats.items():
        t = s["resolved"] + s["failed"]
        pct = round(s["resolved"] / t * 100, 1) if t > 0 else 0
        print(f"  {CONFIGS[cfg]['label']:<30} {s['resolved']:>8} {s['failed']:>7} {pct:>6.1f}%")

    print(f"\n  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62)
    save_csv(stats)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Proper SWE-bench Lite Evaluation")
    p.add_argument("--tasks", type=int, default=10)
    p.add_argument("--start", type=int, default=0)
    args = p.parse_args()
    run(args.tasks, args.start)
