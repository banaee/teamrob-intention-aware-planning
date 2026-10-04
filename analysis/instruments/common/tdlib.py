#!/usr/bin/env python3
"""
COPIED (the sort, 1 October 2026) from analysis/kitting/l_build/tdlib.py (frozen, L-build) as the IRB
instrument's log reader, so that the shared instruments import nothing from a domain's folder; the instruments use
parse(), retired() and inapplicable(). Corrected here (the instruments' own log reading, for dock_loading): the pool and
the winner read by each task's first binding, not by kitting's words (`item`, `ac_switch`, `coffee_machine`; the same
value on every kitting log); the `[IR-inapplicable]` lines (T-G A4) and inapplicable(). The rest of this docstring and runs() / truth() are the L-build original's, unchanged (their
paths name the L-build folder layout).

tdlib.py — the parser and the ground truth the 1.4 / 1.5b / IRB.2b scripts share, rerun for L-build (design_decisions.md,
"T-D L: the belief lifecycle"). Copied from analysis/irb2b_exposed_interval/ (1.4's logic, adapted in 1.5b to the
`leader_adequacy=` field and in IRB.2b to the TD_SIDE switch); changed here for L-build: this docstring, the paths, and
the parse of the L lines: a key may be pinned more than once and re-enter (`[IR-reentry]`), so `pins` and `reentries`
list every (step, key) and `retired(log, key, t)` reads the interval; `complete` keeps the FIRST pin per key (as
before, setdefault); `boundary_action` the action an `[IR-boundary]` names (step -> label, None on the PRE logs);
`[meta-trig]`'s `cause=` (None on the PRE logs and for no_current_task); each decision carries its trigger's cause.

Reads run logs and `.rec` streams only (no simulator import): the POST logs are the four maintained sets regenerated
at L-build (`analysis/<set>/sweep/`), the PRE logs the IRB.2b baselines (md5-identical to the READMEs' "IRB.2b" sections,
48 of 48), copied to `analysis/l_build/pre/<set>/` before the build. Supplementary: `pre/supp/` (HEAD before the build,
identical to IRB.2b's `post/supp/`) and `post/supp/`. All git-ignored.
TD_SIDE=pre runs a script on the PRE logs in place of the POST ones (r["post"] and r["rec"] then name the PRE files),
so that each statistic is computed by the same code on both sides and the two outputs diffed.

Alignment (1.3 report; stated in REPORT.md): the record's ACTION on a tick is the body's action on that tick (lag 0:
`[rec] action=place#0` on the tick of the human's `micro=release`); the record's TASK transitions land 2 ticks after
the world fact the recognizer reads (the release / the last wait tick at t, `completed:` / `entered:` at t + 2).
truth(run, t, lag) reads the record at t + lag: lag 0 is raw, lag 2 the lag-corrected truth.
"""
import math, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
# PRE: `pre/` (the IRB.2b logs, copied before the L-build). POST is always the maintained sets and `post/supp/`.
import os
PRE = os.environ.get("TD_PRE", "pre")
SIDE = os.environ.get("TD_SIDE", "post")   # "pre": the scripts read the PRE logs as their primary side
ROOT = HERE.parents[1]
SETS = ["tb1a_destination", "tb1b_two_tables", "tb1c_realized_flip", "tb3_full_reorder"]
ALPHAS = (0.01, 0.05, 0.1)
THETA, FLOOR, BETA, V = 0.75, 0.001, 0.01, 20.0   # the [run] header's θ, BELIEF_FLOOR, β (/cm), speed (cm/tick)
LAG = 2


# ---- runs ------------------------------------------------------------------------------------------------------
def runs(supp=False):
    """The 48 maintained runs (or, supp=True, the four supplementary wrong-table runs), each a dict."""
    out = []
    if supp:
        for p in sorted((HERE / "post" / "supp").glob("*.log")):
            out.append(_run("supp", p, HERE / PRE / "supp" / p.name))
        return out
    for s in SETS:
        for p in sorted((ROOT / "analysis" / s / "sweep").glob("*.log")):
            out.append(_run(s, p, HERE / PRE / s / p.name))
    return out


def _run(set_, post, pre):
    if SIDE == "pre":
        post = pre
    stem = post.stem
    m = re.match(r"(env_layout_\d+)_(scenario_s\d+_\d+)_(.*)$", stem)
    opts = m[3].split("_")
    return dict(set=set_, name=stem, layout=m[1], scenario=m[2], prior=opts[-1], opts="_".join(opts[:-1]) or "-",
                post=post, pre=pre, rec=post.with_suffix(".rec"), prerec=pre.with_suffix(".rec"))


def label(r):
    return f"{r['scenario']} {r['opts'] if r['opts'] != '-' else ''} {r['prior']}".replace("  ", " ")


# ---- log parsing -----------------------------------------------------------------------------------------------
IR = re.compile(r"\[IR\] step=(\d+) most_likely=(\S+) confidence=(\S+)"
                r"(?: lifecycle=(\S+))?(?: finding=(\S+))?(?: leader_adequacy=(\S+))?(?: tails=\[(.*)\])?")
DIST = re.compile(r"\[IR-dist\] step=(\d+) most_likely=(\S+) confidence=(\S+) dist=\[(.*)\]")
AGENT = re.compile(r"\s*step: (\d+): \[(human_\d+|robot_\d+)\] task=(\S+) action=(\S+) micro=(\S+) "
                   r"pos=\[\s*(\S+)\s+(\S+)\s*\]")
REC = re.compile(r"\[rec\] step=(\d+) stack=(.*?) action=(\S+) progress=(\S+) events=(\S+)$")


def _kv(s):
    """'k1=v1  k2=v2' with keys that contain '=' -> {k: float(v)}."""
    out = {}
    for tok in s.split():
        k, v = tok.rsplit("=", 1)
        out[k] = float(v)
    return out


def parse(path):
    """
    One run log. Returns a dict:
      ir        step -> dict(ml, conf, lifecycle, finding, lead, tails{key: S}) ([IR]; lead, the leader's hypothesis
                adequacy, None in the PRE logs and when exhausted)
      dist      step -> {key: P} ([IR-dist], three decimals)
      complete  key -> the first step ([IR-complete]); boundary: [IR-boundary] steps
      pins, reentries  every [IR-complete] / [IR-reentry] as (step, key), in log order
      boundary_action  step -> the action an [IR-boundary] names (None on the PRE logs)
      triggers  every [meta-trig]: (step, trigger, cause)
      known     the [IR-assignment] known list (strings, as logged; `[IR-prior] switch=` before T-K part 1's
                rename, AM9); prior 'on' | 'off' (the assignment knowledge)
      context   step -> dict(facts [str], recent [task names], levels {task name: level}, prior {key: pi, 4 decimals})
                from the [IR-context] lines (T-K part 1, stage 5; absent with context knowledge off)
      timeline  the `[run_mesa] timeline source=... windows=[...]` line's text after the tag (None before stage 4)
      coverage  task string -> coverage value ([coverage] lines)
      human, robot  step -> (action, micro, (x, y), task)
      decisions list of dict(step, trigger, proj, conf_proj, winner, queue, b3, holds) — one per [meta] line
      holds     every [hold] line parsed: (step, kind, fields)
      done      the empty-pool step ([meta] ... all tasks complete) or None
      header    the [run] key=value fields
    """
    ir, dist, complete, boundary, cov = {}, {}, {}, [], {}
    pins, reentries, boundary_action, triggers = [], [], {}, []
    inapplicable = []
    cause = None
    human, robot = {}, {}
    decisions, holds = [], []
    known, prior, header, done = [], None, {}, None
    context, timeline = {}, None
    trig = proj = b3 = None
    for l in open(path, errors="replace"):
        l = l.rstrip("\n")
        if l.startswith("[IR] "):
            m = IR.match(l)
            s = int(m[1])
            ir[s] = dict(ml=m[2], conf=float(m[3]), lifecycle=m[4], finding=m[5], lead=m[6],
                         tails=_kv(m[7]) if m[7] else {})
        elif l.startswith("[IR-dist]"):
            m = DIST.match(l)
            dist[int(m[1])] = _kv(m[4])
        elif l.startswith("[IR-complete]"):
            m = re.match(r"\[IR-complete\] step=(\d+) (\S+) completed", l)
            complete.setdefault(m[2], int(m[1]))
            pins.append((int(m[1]), m[2]))
        elif l.startswith("[IR-reentry]"):
            m = re.match(r"\[IR-reentry\] step=(\d+) (\S+) live again", l)
            reentries.append((int(m[1]), m[2]))
        elif l.startswith("[IR-inapplicable]"):
            m = re.match(r"\[IR-inapplicable\] step=(-?\d+) (\S+) (?:does not enter|leaves) the live set", l)
            inapplicable.append((int(m[1]), m[2]))
        elif l.startswith("[IR-boundary]"):
            m = re.match(r"\[IR-boundary\] step=(\d+) \S+ completed (a task|\S+?):", l)
            boundary.append(int(m[1]))
            boundary_action[int(m[1])] = None if m[2] == "a task" else m[2]
        elif l.startswith("[IR-assignment]"):
            prior = re.search(r"knowledge=(\w+)", l)[1]
            known = re.findall(r"'([^']+)'", l)
        elif l.startswith("[IR-context]"):
            m = re.match(r"\[IR-context\] step=(-?\d+) facts=\[(.*?)\] recent=\[(.*?)\] levels=\[(.*?)\] prior=\[(.*)\]$", l)
            context[int(m[1])] = dict(facts=m[2].split(), recent=m[3].split(),
                                      levels=dict(x.split("=") for x in m[4].split()), prior=_kv(m[5]) if m[5] else {})
        elif l.startswith("[run_mesa] timeline "):
            timeline = l[len("[run_mesa] timeline "):]
        elif l.startswith("[coverage]"):
            m = re.match(r"\[coverage\] \S+ \S+ entry=\d+ (\S+?\))=(\S+)$", l)
            cov[m[1]] = m[2]
        elif l.startswith("[run] "):
            header = dict(re.findall(r"(\w+)=(\S+)", l))
        elif l.startswith("[meta-trig]"):
            m = re.match(r"\[meta-trig\] step=(\d+) trigger=(\S+)(?: cause=(\S+))?", l)
            trig = (int(m[1]), m[2]); proj = b3 = None; cause = m[3]
            triggers.append((int(m[1]), m[2], m[3]))
        elif l.startswith("[meta-proj]"):
            m = re.match(r"\[meta-proj\] confidence=(\S+) theta=\S+ projection=(\S+)", l)
            proj = (float(m[1]), m[2])
        elif l.startswith("[meta-b3]"):
            b3 = dict(re.findall(r"(\w+)=(\S+)", l))
        elif l.startswith("[meta] "):
            m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
            if m:
                done = int(m[1]); continue
            m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=(\S+\{[^}]*\})(?: queue=(.*))?", l)
            decisions.append(dict(step=int(m[1]), trigger=m[2], cause=cause, winner=short(m[3]),
                                  queue=tuple(re.findall(r"\{'\?[^']+': '([^']+)'", m[4] or "")),
                                  proj=proj[1] if proj else None, conf_proj=proj[0] if proj else None,
                                  selection=(b3 or {}).get("selection"), hold=(b3 or {}).get("hold"),
                                  ordering=(b3 or {}).get("ordering")))
        elif l.startswith("[hold]"):
            m = re.match(r"\[hold\] step=(\d+) \S+ (\w+) (.*)$", l)
            holds.append((int(m[1]), m[2], dict(re.findall(r"(\w+)=(\S+)", m[3]))))
        else:
            m = AGENT.match(l)
            if m:
                d = human if m[2].startswith("human") else robot
                d[int(m[1])] = (m[4], m[5], (float(m[6]), float(m[7])), m[3])
    return dict(ir=ir, dist=dist, complete=complete, boundary=boundary, known=known, prior=prior, coverage=cov,
                human=human, robot=robot, decisions=decisions, holds=holds, done=done, header=header,
                pins=pins, reentries=reentries, boundary_action=boundary_action, triggers=triggers,
                inapplicable=inapplicable, context=context, timeline=timeline)


def retired(log, key, t):
    """Whether `key` is retired (pinned) on tick t: its last [IR-complete] at or before t is later than its last
    [IR-reentry] at or before t (T-D L4: retired while its terminal fact holds)."""
    pin = max((s for s, k in log["pins"] if k == key and s <= t), default=None)
    back = max((s for s, k in log["reentries"] if k == key and s <= t), default=None)
    return pin is not None and (back is None or pin > back)


def inapplicable(log, key, t):
    """Whether `key` is out of the live set on tick t for want of an applicable method (T-G A4): its last
    [IR-inapplicable] at or before t is later than its last [IR-reentry] at or before t."""
    out = max((s for s, k in log["inapplicable"] if k == key and s <= t), default=None)
    back = max((s for s, k in log["reentries"] if k == key and s <= t), default=None)
    return out is not None and (back is None or out > back)


def short(w):
    """A [meta] winner dict string -> the value of its first binding ('item_3', 'pallet_0', 'coffee_machine_0')."""
    m = re.search(r"\{'\?[^']+': '([^']+)'", w)
    return m[1] if m else w


def parse_rec(path):
    """step -> dict(top, action, progress, events); top None on the empty stack."""
    out = {}
    for l in open(path):
        m = REC.match(l.rstrip("\n"))
        if not m:
            continue
        stack = m[2]
        top = None if stack == "-" else _first_task(stack)
        out[int(m[1])] = dict(top=top, action=None if m[3] == "-" else m[3], progress=m[4],
                              events=[] if m[5] == "-" else _split(m[5]))
    return out


def _split(s):
    """A ','-joined list of 'name(args)' items, split at depth 0."""
    out, depth, start = [], 0, 0
    for i, c in enumerate(s):
        depth += c == "("
        depth -= c == ")"
        if c == "," and depth == 0:
            out.append(s[start:i]); start = i + 1
    return out + [s[start:]]


def _first_task(stack):
    """The first task of a stack string (tasks are 'name(args)', joined by ',' at depth 0)."""
    return _split(stack)[0]


# ---- keys and truth --------------------------------------------------------------------------------------------
def key_of(task):
    """The hypothesis key the logs print for a COVERED task string (the item's table is not printed)."""
    return re.sub(r",\?kitting_table=kitting_table_\d+", "", task)


def truth(log, rec, t, lag=0):
    """
    The record's truth at tick t read at t + lag: dict(task, action, phase, cov, key). key is the hypothesis key when
    the task is COVERED, else None; task None on the empty stack. phase: the action name without its occurrence.
    """
    last = max(rec)
    r = rec[min(t + lag, last)]
    task = r["top"]
    if task is None:
        return dict(task=None, action=None, phase=None, cov="no_task", key=None)
    cov = log["coverage"].get(task, "?")
    return dict(task=task, action=r["action"], phase=r["action"].split("#")[0] if r["action"] else None,
                cov=cov, key=key_of(task) if cov == "covered" else None)


def finding_at(ir_t, alpha):
    """The finding recomputed from the logged (4-decimal) tails at test level alpha; 'exhausted' when exhausted."""
    if ir_t["lifecycle"] == "exhausted":
        return "exhausted"
    if not ir_t["tails"]:
        return "unresolved"
    return "unexplained" if all(s < alpha for s in ir_t["tails"].values()) else "adequate"


def vd_of(S):
    """v·D (cm) from a tail S (the inverse of S(x) = ln(1 + e^(-βx)) / ln 2); 0 for S = 1."""
    if S >= 1.0:
        return 0.0
    if S <= 0.0:
        return math.inf
    return -math.log(2.0 ** S - 1.0) / BETA


def human_events(log):
    """Per human action instance on the body: arrival (last walking tick of a move_to), grasp, release, wait end."""
    ev = []
    h = log["human"]
    steps = sorted(h)
    for i, s in enumerate(steps):
        a, mu = h[s][:2]
        if mu == "grasp":
            ev.append((s, "grasp"))
        elif mu == "release":
            ev.append((s, "release"))
        nxt = h.get(s + 1)
        if a == "move_to" and mu == "step" and nxt is not None and nxt[1] != "step":
            ev.append((s, "arrival"))
        if a == "wait_at" and nxt is not None and nxt[0] != "wait_at":
            ev.append((s, "wait_end"))
    return ev


def robot_completion(log):
    """T6: the world completion tick, the tick after the robot's last release (None if it never released). Only
    releases with a task count: after its pool empties the robot's line keeps showing place/release with task=None."""
    rel = [s for s, (a, mu, _, task) in log["robot"].items() if a == "place" and mu == "release" and task != "None"]
    return max(rel) + 1 if rel else None


def fmt(x, n=3):
    return "-" if x is None else f"{x:.{n}f}"


def ir_groups(rs):
    """Runs grouped by identical recognizer output and ground truth: the [IR*] lines and the .rec stream."""
    import hashlib
    groups = {}
    for r in rs:
        h = hashlib.md5()
        for l in open(r["post"], errors="replace"):
            if l.startswith("[IR"):
                h.update(l.encode())
        h.update(open(r["rec"], "rb").read())
        groups.setdefault(h.hexdigest(), []).append(r)
    return list(groups.values())
