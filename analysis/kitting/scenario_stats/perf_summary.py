# analysis/kitting/scenario_stats/perf_summary.py
"""The tables of the performance statistics from perf.py's rows: python perf_summary.py <perf.json> <rows.json>"""
import json, sys, collections, statistics as st

rows = json.load(open(sys.argv[1]))
pool = {x['id']: x['robot_tasks'] for x in json.load(open(sys.argv[2]))}   # extract.py's rows: the robot's pool size

def q(v, p):
    v = sorted(v); i = (len(v) - 1) * p; lo = int(i); hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)

def line(label, v, fmt='{:.0f}'):
    if not v: print(f"| {label} | 0 | | | | | | | |"); return
    f = lambda x: fmt.format(x)
    print(f"| {label} | {len(v)} | {f(min(v))} | {f(q(v, .1))} | {f(st.median(v))} | {st.mean(v):.1f} | {f(q(v, .9))} | {f(max(v))} | {st.pstdev(v):.1f} |")

def head(first):
    print(f"| {first} | n | min | p10 | median | mean | p90 | max | sd |"); print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

def hist(v, width):
    c = collections.Counter(int(x // width) * width for x in v)
    return ", ".join(f"{b}–{b + width - 1}: {c[b]}" for b in sorted(c))

TYPES = ['deliver_item', 'coffee_break', 'ac_activation', 'go_to', 'stand', 'go_to_and_stand']
tasks = [t for r in rows for t in r['tasks']]
print("## Runs\n")
print(f"runs {len(rows)}; steps (the safety cap) min {min(r['steps'] for r in rows)}, median {st.median(r['steps'] for r in rows)}, max {max(r['steps'] for r in rows)}")
print(f"task instances in the records {len(tasks)}: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(t['outcome'] for t in tasks).items()))
print("\n## H1. The human's ticks per task (completed instances; ticks with the task on top of the stack)\n")
head('task type')
for ty in TYPES: line(ty, [t['active'] for t in tasks if t['type'] == ty and t['outcome'] == 'completed'])
print("\nSpan, entered to completed, of the instances that were suspended (the time under the interrupting task included):\n")
head('task type')
for ty in TYPES:
    v = [t['span'] for t in tasks if t['type'] == ty and t['outcome'] == 'completed' and t['suspended']]
    if v: line(ty, v)
print("\nAbandoned instances (a drop), ticks on top before the drop:\n")
head('task type')
for ty in TYPES:
    v = [t['active'] for t in tasks if t['type'] == ty and t['outcome'] == 'abandoned']
    if v: line(ty, v)
print("\nInstances started by an event (a switch), completed:\n")
head('task type')
for ty in TYPES:
    v = [t['active'] for t in tasks if t['type'] == ty and t['outcome'] == 'completed' and t['started_by_event']]
    if v: line(ty, v)
print("\nDistribution, completed instances, bins of 10 ticks:\n")
for ty in TYPES:
    v = [t['active'] for t in tasks if t['type'] == ty and t['outcome'] == 'completed']
    print(f"- {ty}: {hist(v, 10)}")
print("\n## H2. The human's ticks per action occurrence (its acknowledgement tick included)\n")
acts = collections.defaultdict(list)
for r in rows:
    for a, n in r['actions']: acts[a].append(n)
head('action')
for a in sorted(acts): line(a, acts[a])
print("\n## H3. The human's script length (ticks until the last task closes)\n")
v = [r['human_last_busy'] for r in rows]
head('measure'); line('script length', v)
print(f"\nBins of 50: {hist(v, 50)}")
print("\nShare of the human's busy ticks per task type (all runs pooled):\n")
tot = sum(t['active'] for t in tasks)
for ty in TYPES:
    s = sum(t['active'] for t in tasks if t['type'] == ty); print(f"- {ty}: {s} ticks, {100 * s / tot:.1f}%")
print("\n## R1. The recognizer's leader against the task in hand (task-model types; per instance)\n")
print("Share of the instance's ticks on top of the stack in which the recognizer's most likely hypothesis is the task:\n")
head('task type')
for ty in TYPES[:3]: line(ty, [t['leader_share'] for t in tasks if t['type'] == ty and 'leader_share' in t], '{:.2f}')
print("\nTicks from the instance's first tick on top until the leader is first the task (instances never led: count):\n")
head('task type')
for ty in TYPES[:3]:
    w = [t for t in tasks if t['type'] == ty and 'leader_share' in t]
    line(ty, [t['leader_first'] for t in w if t['leader_first'] is not None])
    print(f"| {ty}: never the leader | {sum(t['leader_first'] is None for t in w)} | | | | | | | |")
work = [r for r in rows if pool[r['scenario']] > 0]
idle = [r for r in rows if r not in work]
print(f"\n## P1. The robot (working robot: {len(work)} runs; idle robot: {len(idle)} runs)\n")
print(f"pool completed within the cap: {sum(r['robot_pool_complete'] and r['robot_complete'] is not None for r in work)} of {len(work)}\n")
head('measure')
line('completion tick (world)', [r['robot_complete'] for r in work if r['robot_complete'] is not None])
line('releases done (b)', [r['robot_tasks_done'] for r in work])
D = [d for r in work for d in r['deliveries']]
line('ticks per delivery, total', [sum(d.values()) for d in D])
line('… walking (step)', [d.get('step', 0) for d in D])
line('… standing in a task (holds)', [d.get('stand', 0) for d in D])
line('… grasp and release', [d.get('grasp_release', 0) for d in D])
line('… acknowledgement ticks', [d.get('ack', 0) for d in D])
line('ticks without a task before completion', [r['robot_idle_before_completion'] for r in work if 'robot_idle_before_completion' in r])
line('holds per run', [r['holds'] for r in work])
line('held ticks per run', [r['hold_ticks'] for r in work])
line('admissions (projection built)', [r['admissions'] for r in work])
line('fallback projections', [r['fallbacks'] for r in work])
for tr in ['no_current_task', 'recognition_changed', 'projection_expired']:
    line(f'decisions: {tr}', [r['triggers'].get(tr, 0) for r in work])
line('decisions: all', [sum(r['triggers'].values()) for r in work])
line('separation minimum (cm)', [r['sep_min'] for r in work if r['sep_min'] is not None])
line('ticks below min_separation (50 cm)', [r['sep_below50'] for r in work])
print(f"\nruns with a tick below min_separation: {sum(r['sep_below50'] > 0 for r in work)} of {len(work)}")
print(f"completion tick, bins of 50: {hist([r['robot_complete'] for r in work if r['robot_complete'] is not None], 50)}")
print(f"\nIdle robot: ticks below min_separation in {sum(r['sep_below50'] > 0 for r in idle)} of {len(idle)} runs; separation minimum median {st.median([r['sep_min'] for r in idle if r['sep_min'] is not None]):.1f} cm")
