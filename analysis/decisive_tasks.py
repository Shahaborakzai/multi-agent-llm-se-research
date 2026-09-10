import json, collections

tc = collections.defaultdict(dict)
for line in open('experiments/eval_results.jsonl'):
    try:
        r = json.loads(line)
        tc[r['task_id']][r['config']] = r['passed']
    except: pass

cfgs = ['baseline','coder','coder_tester','full_system']
print("Tasks where configurations disagree (19 total):")
print("-" * 65)
rescued, lost = [], []
for tid, d in sorted(tc.items()):
    outcomes = [d.get(c,False) for c in cfgs]
    if len(set(outcomes)) > 1:
        if not d.get('baseline') and any(d.get(c) for c in cfgs[1:]):
            rescued.append(tid)
        elif d.get('baseline') and any(not d.get(c) for c in cfgs[1:]):
            lost.append(tid)
        row = ' | '.join(f"{'P' if d.get(c) else 'F'}" for c in cfgs)
        print(f"{tid:<25} {row}")
print(f"\nRescued by roles: {len(rescued)}")
print(f"Lost by roles:    {len(lost)}")
