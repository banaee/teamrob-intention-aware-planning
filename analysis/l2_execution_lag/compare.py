#!/usr/bin/env python3
"""
compare.py — T9 regression comparison: baseline/ (aefebc7, projection walks to the target point)
vs new/ (HEAD, projection ends at the body's arrival radius). Ten conditions.
Per condition: the decision sequence ([meta] winners per trigger, [meta-proj] reasons, [meta-pool]
drops), the first tick at which any [IR]/[IR-dist] line differs, the first [meta] difference, every
[meta-cand] line that changed (cost / feasible / min_dist) at triggers whose decision is unchanged,
whether the log minus [meta-cand] and [sep] lines is otherwise identical, and the actual
robot–human separation (from the new [sep] lines; from the per-tick position lines in the baseline).
Writes comparison.md next to this file.
Usage: python analysis/l2_execution_lag/compare.py [baseline_dir] [new_dir]
"""
import re, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "t9_arrival_radius", "new")
NEW = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "new")
CONDS = ["s00_off", "s00_on", "s10_off", "s10_on", "s20_off", "s20_on", "s30_off", "s30_on", "s40_off", "s40_on"]
STEP = re.compile(r"step=(\d+)")
POS = re.compile(r"^  step: (\d+): \[(\w+)\] .* pos=\[\s*([-\d.]+)\s+([-\d.]+)\s*\]")
SEP = re.compile(r"^\[sep\] step=(\d+) \S+ dist=([\d.]+)")
MIN_SEPARATION = 50.0   # 2.5 x 20 cm/tick (R1, TODO-28) — the value later tasks report against

def read(cond, which):
    with open(os.path.join(BASE if which == "baseline" else NEW, cond + ".log")) as f:
        return f.read().splitlines()

def short(line):
    return (line.replace(",?kitting_table=kitting_table_0", "")
                .replace(", '?kitting_table': 'kitting_table_0'", "")
                .replace("deliver_item{'?item': '", "deliver_item(").replace("'}", ")"))

def decisions(lines):
    out, step = [], None
    for ln in lines:
        if ln.startswith("[meta-trig]"):
            step = int(STEP.search(ln).group(1)); continue
        if ln.startswith("[meta-proj]"):
            out.append((step, "proj", ln.split("projection=")[1]))
        elif ln.startswith("[meta-pool]"):
            out.append((step, "pool", short(ln[len("[meta-pool] "):])))
        elif ln.startswith("[meta] "):
            m = re.match(r"\[meta\] step=(\d+) (?:trigger=(\S+) winner=(\S+?) queue=(.*)|(all tasks complete))", short(ln))
            if m.group(5):
                out.append((int(m.group(1)), "meta", "all tasks complete"))
            else:
                out.append((int(m.group(1)), "meta", f"{m.group(2)} -> {m.group(3)} queue={m.group(4)}"))
    return out

def cands(lines):
    """[meta-cand] lines grouped by trigger step."""
    out, step = {}, None
    for ln in lines:
        if ln.startswith("[meta-trig]"):
            step = int(STEP.search(ln).group(1)); continue
        if ln.startswith("[meta-cand]"):
            out.setdefault(step, []).append(short(ln))
    return out

def ir_lines(lines):
    return [ln for ln in lines if ln.startswith("[IR] ") or ln.startswith("[IR-dist] ")]

def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, x, y
    if len(a) != len(b):
        return min(len(a), len(b)), (a[len(b)] if len(a) > len(b) else None), (b[len(a)] if len(b) > len(a) else None)
    return None

def separation(lines):
    """Per-tick robot_0–human_0 distance: from [sep] lines if present, else from the position lines."""
    seps = {int(m.group(1)): float(m.group(2)) for m in (SEP.match(ln) for ln in lines) if m}
    if seps:
        return seps
    pos = {}
    for ln in lines:
        m = POS.match(ln)
        if m:
            pos.setdefault(int(m.group(1)), {})[m.group(2)] = (float(m.group(3)), float(m.group(4)))
    return {s: math.hypot(p["robot_0"][0] - p["human_0"][0], p["robot_0"][1] - p["human_0"][1])
            for s, p in pos.items() if "robot_0" in p and "human_0" in p}

def sep_summary(seps):
    if not seps:
        return "n/a"
    m = min(seps.values()); t = min(s for s, d in seps.items() if d == m)
    below = sorted(s for s, d in seps.items() if d < MIN_SEPARATION)
    runs = []
    for s in below:
        if runs and s == runs[-1][1] + 1: runs[-1][1] = s
        else: runs.append([s, s])
    return (f"min {m:.1f} cm at step {t}; ticks below {MIN_SEPARATION:.0f} cm: {len(below)} of {len(seps)}"
            + (f" (runs {', '.join(f'{a}–{b}' if a != b else str(a) for a, b in runs)})" if runs else ""))

rows = ["# L2 sweep comparison — baseline (T9 baselines: no completion latency, human projection at step 0) vs new (HEAD: per-action completion latency, human projection at the observation offset)", "",
        "PYTHONHASHSEED=0, ten conditions. `-` = baseline only, `+` = new only; unchanged decisions are not listed.", ""]
for cond in CONDS:
    base, new = read(cond, "baseline"), read(cond, "new")
    db, dn = decisions(base), decisions(new)
    ib, inew = ir_lines(base), ir_lines(new)
    fd = first_diff(ib, inew)
    rows.append(f"## {cond}"); rows.append("")
    metas_b = [d for d in db if d[1] == "meta"]; metas_n = [d for d in dn if d[1] == "meta"]
    fm = first_diff(metas_b, metas_n)
    rows.append(f"- first [meta] difference: " + (f"step {fm[1][0] if fm[1] else fm[2][0]}" if fm else "none"))
    if fd is None:
        rows.append(f"- [IR]/[IR-dist] lines: byte-identical ({len(ib)} lines)")
    elif fd[2] is None or fd[1] is None:
        rows.append(f"- [IR]/[IR-dist] lines: one is a prefix of the other ({len(inew)} new / {len(ib)} baseline lines)")
    else:
        sb = STEP.search(fd[1] or fd[2] or "").group(1)
        rows.append(f"- [IR]/[IR-dist] lines: identical up to step {int(sb)-1}, first difference at step {sb} (line {fd[0]} of {len(ib)} / {len(inew)})")
    rows.append(f"- run end: baseline {metas_b[-1][0]}, new {metas_n[-1][0]} (last [meta] step)")
    strip = lambda ls: [ln for ln in ls if not (ln.startswith("[meta-cand]") or ln.startswith("[sep]"))]
    nb, nn = strip(base), strip(new)
    rows.append(f"- full log minus [meta-cand] and [sep] lines: {'byte-identical' if nb == nn else 'DIFFERS'} ({len(nb)} / {len(nn)} lines)")
    rows.append(f"- actual robot–human separation, baseline: {sep_summary(separation(base))}")
    rows.append(f"- actual robot–human separation, new:      {sep_summary(separation(new))}")
    rows.append("")
    sb_, sn_ = set(db), set(dn)
    removed = [d for d in db if d not in sn_]; added = [d for d in dn if d not in sb_]
    if not removed and not added:
        rows.append("decision sequence unchanged.")
    else:
        rows.append("```")
        for d in sorted(removed + added, key=lambda d: (d[0], d in added)):
            rows.append(f"{'+' if d in added else '-'} step={d[0]:<4} {d[1]:<5} {d[2]}")
        rows.append("```")
    cb, cn = cands(base), cands(new)
    changed = [(s, cb.get(s, []), cn.get(s, [])) for s in sorted(set(cb) | set(cn)) if cb.get(s) != cn.get(s)]
    if changed:
        rows.append(""); rows.append(f"[meta-cand] lines that differ ({len(changed)} of {len(set(cb) | set(cn))} triggers):"); rows.append("```")
        for s, a, b in changed:
            for x in a: rows.append(f"- step={s:<4} {x[len('[meta-cand] '):]}")
            for x in b: rows.append(f"+ step={s:<4} {x[len('[meta-cand] '):]}")
        rows.append("```")
    rows.append("")
open(os.path.join(HERE, "comparison.md"), "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
