import json, numpy as np, collections
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.dummy import DummyClassifier

tasks = {json.loads(l)['task_id']: json.loads(l)
         for l in open('workspace/HumanEval.jsonl') if l.strip()}
tc = collections.defaultdict(dict)
for l in open('experiments/eval_results.jsonl'):
    try:
        r = json.loads(l); tc[r['task_id']][r['config']] = r['passed']
    except: pass

def feats(p):
    w = p.split()
    return [len(p.strip().split('\n')), len(w), len(p), p.count('->'),
            p.count('List'), p.count('Dict'), p.count('Optional'),
            p.count('"""'), p.count('>>>'), p.count('\n    '),
            len([x for x in w if len(x)>8]),
            p.count('int')+p.count('float')+p.count('str')]

order = ['baseline','coder','coder_tester','full_system']
X, y = [], []
for t, cfgs in tc.items():
    if t not in tasks: continue
    X.append(feats(tasks[t]['prompt']))
    y.append(next((c for c in order if cfgs.get(c)), 'baseline'))

X, y = np.array(X), np.array(y)
cv = StratifiedKFold(5, shuffle=True, random_state=42)
mc = cross_val_score(DummyClassifier(strategy='most_frequent'), X, y, cv=cv).mean()
dt = cross_val_score(DecisionTreeClassifier(max_depth=4, random_state=42), X, y, cv=cv).mean()
print(f"Majority-class baseline: {mc:.3f} ({mc*100:.1f}%)")
print(f"Decision Tree:           {dt:.3f} ({dt*100:.1f}%)")
print(f"Margin:                  {(dt-mc)*100:+.1f} pp")
