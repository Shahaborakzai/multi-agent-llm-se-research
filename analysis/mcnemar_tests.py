import json, collections
from itertools import combinations
from scipy.stats import binomtest

res = collections.defaultdict(dict)
for line in open('experiments/swe_results_FINAL.jsonl'):
    try:
        r = json.loads(line)
        res[r['config']][r['task_id']] = r['resolved']
    except: pass

print("Pairwise McNemar tests — SWE-bench Lite (n=30)")
print("-" * 55)
for a, b in combinations(res, 2):
    shared = set(res[a]) & set(res[b])
    b01 = sum(1 for t in shared if not res[a][t] and res[b][t])
    b10 = sum(1 for t in shared if res[a][t] and not res[b][t])
    n = b01 + b10
    p = binomtest(b01, n, 0.5).pvalue if n > 0 else 1.0
    print(f"{a} vs {b}: discordant={n}, p={p:.4f}")
