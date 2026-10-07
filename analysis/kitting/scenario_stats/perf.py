# analysis/kitting/scenario_stats/perf.py
"""Per-run performance counts from a run's .log and .rec: the human's ticks per task and per action, the recognizer's
leader against the task in hand, the robot's ticks per delivery and its decisions. python perf.py <runs dir> <out.json>"""
import json, re, sys, collections
from pathlib import Path

EV = re.compile(r'(entered|completed|abandoned|started|suspended|resumed):([a-z_]+)\(([^)]*)\)')
REC = re.compile(r'^\[rec\] step=(\d+) stack=(\S+) action=(\S+) progress=(\d+)/(\d+) events=(.*)$')
IR = re.compile(r'^\[IR\] step=(\d+) most_likely=(\S+)')
ROB = re.compile(r'step: (\d+): \[robot_0\] task=(\S+) action=(\S+) micro=(\S+)')

def key(name, args):
    return name, frozenset(a for a in args.split(',') if a)

def parse_key(s):
    m = re.match(r'([a-z_]+)\(([^)]*)\)$', s)
    return key(m.group(1), m.group(2)) if m else None

def run(log, rec):
    out = {'scenario': log.stem}
    # --- the human: the record
    tops, actions, inst, cur_of = [], [], [], {}
    for line in open(rec):
        m = REC.match(line)
        if not m: continue
        t, stack, act, k, n, evs = int(m[1]), m[2], m[3], int(m[4]), int(m[5]), m[6]
        for kind, name, args in EV.findall(evs):
            kk = key(name, args)
            if kind == 'entered' or kk not in cur_of:
                inst.append({'key': kk, 'type': name, 'events': [], 'ticks': []}); cur_of[kk] = len(inst) - 1
            inst[cur_of[kk]]['events'].append((kind, t))
        top = None if stack == '-' else parse_key(re.match(r'([a-z_]+\([^)]*\))', stack)[1])
        if top is not None and top in cur_of: inst[cur_of[top]]['ticks'].append(t)
        tops.append(top); actions.append((top, act, k))
    steps = len(tops)
    busy = [t for t, x in enumerate(tops) if x is not None]
    out['steps'] = steps
    out['human_last_busy'] = (busy[-1] + 1) if busy else 0
    leader = {}
    for line in open(log):
        m = IR.match(line)
        if m: leader[int(m[1])] = parse_key(m[2])
    tasks = []
    for i in inst:
        k = i['key']; ev = dict()
        for kind, t in i['events']: ev.setdefault(kind, t)
        end = ev.get('completed', ev.get('abandoned'))
        ticks = i['ticks']
        rec = {'type': i['type'], 'outcome': 'completed' if 'completed' in ev else 'abandoned' if 'abandoned' in ev else 'open',
               'active': len(ticks), 'span': (end - ev['entered']) if end is not None and 'entered' in ev else None,
               'suspended': 'suspended' in ev, 'started_by_event': 'started' in ev}
        if ticks and any(t in leader for t in ticks):
            right = [t for t in ticks if leader.get(t) and leader[t][0] == k[0] and leader[t][1] <= k[1]]
            rec['leader_share'] = len(right) / len(ticks)
            rec['leader_first'] = (right[0] - ticks[0]) if right else None
        tasks.append(rec)
    out['tasks'] = tasks
    # per action occurrence: rows of the same (top, action label) starting at progress 1
    acts, cur, prev_k = [], None, 0
    for top, act, k in actions:
        if act == '-': cur = None; continue
        if cur is None or cur[0] != (top, act) or k < prev_k:
            cur = [(top, act), 0]; acts.append(cur)
        cur[1] += 1; prev_k = k
    out['actions'] = [(a[0][1].split('#')[0], a[1]) for a in acts]
    # --- the robot: the log
    rob = []
    for line in open(log):
        m = ROB.search(line)
        if m: rob.append((int(m[1]), m[2], m[3], m[4]))
    complete = None
    for line in open(log):
        m = re.match(r'^\[meta\] step=(\d+) all tasks complete', line)
        if m: complete = int(m[1])
    releases = [t for t, task, a, mi in rob if task != 'None' and a == 'place' and mi == 'release']
    out['robot_tasks_done'] = len(releases)
    out['robot_complete'] = (releases[-1] + 1) if (complete is not None and releases) else None
    out['robot_pool_complete'] = complete is not None
    dels, c = [], collections.Counter()
    for t, task, a, mi in rob:
        if releases and t > releases[-1] + 1: break
        if task == 'None':
            continue
        c['step' if mi == 'step' else 'stand' if mi == 'stand' else 'grasp_release' if mi in ('grasp', 'release') else 'ack'] += 1
        if a == 'place' and mi == 'None':
            dels.append(dict(c)); c = collections.Counter()
    out['deliveries'] = dels
    if releases:
        out['robot_idle_before_completion'] = sum(1 for t, task, a, mi in rob if t <= releases[-1] and task == 'None')
    trig = collections.Counter()
    for line in open(log):
        m = re.match(r'^\[meta\] step=\d+ trigger=([a-z_]+)', line)
        if m: trig[m[1]] += 1
    out['triggers'] = dict(trig)
    out['admissions'] = sum(1 for l in open(log) if l.startswith('[meta-proj]') and 'projection=built' in l)
    out['fallbacks'] = sum(1 for l in open(log) if l.startswith('[meta-proj]') and 'projection=fallback' in l)
    seps = [float(m[1]) for l in open(log) for m in [re.match(r'^\[sep\] step=\d+ \S+ dist=([\d.]+)', l)] if m]
    out['sep_min'] = min(seps) if seps else None
    out['sep_below50'] = sum(1 for d in seps if d < 50)
    holds = [int(m[1]) for l in open(log) for m in [re.search(r'^\[hold\].* end planned=\d+ executed=(\d+)', l)] if m]
    out['holds'] = len(holds); out['hold_ticks'] = sum(holds)
    return out

d = Path(sys.argv[1])
rows = [run(l, l.with_suffix('.rec')) for l in sorted(d.glob('*.log'))]
json.dump(rows, open(sys.argv[2], 'w'))
print(len(rows))
