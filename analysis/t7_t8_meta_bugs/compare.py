#!/usr/bin/env python3
"""
compare.py — T7/T8 regression comparison: baseline/ (adf9aea, before the fixes) vs new/ (HEAD).
Per condition: the decision sequence ([meta] winners per trigger, [meta-proj] reasons, [meta-pool]
drops), the first tick at which any [IR]/[IR-dist] line differs, and the first [meta] difference.
Writes summary.md next to this file. Usage: python analysis/t7_t8_meta_bugs/compare.py
"""
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CONDS = ["s00_off", "s00_on", "s20_off", "s20_on", "s30_off", "s30_on", "s40_off", "s40_on"]
STEP = re.compile(r"step=(\d+)")

def read(cond, which):
    with open(os.path.join(HERE, which, cond + ".log")) as f:
        return f.read().splitlines()

def short(line):
    return (line.replace(",?kitting_table=kitting_table_0", "")
                .replace(", '?kitting_table': 'kitting_table_0'", "")
                .replace("deliver_item{'?item': '", "deliver_item(").replace("'}", ")"))

def decisions(lines):
    """[meta-trig]-anchored events: every fired trigger with its [meta-proj] reason, [meta-pool]
    drops, and [meta] outcome, keyed by step."""
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

def ir_lines(lines):
    return [ln for ln in lines if ln.startswith("[IR] ") or ln.startswith("[IR-dist] ")]

def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, x, y
    if len(a) != len(b):
        return min(len(a), len(b)), (a[len(b)] if len(a) > len(b) else None), (b[len(a)] if len(b) > len(a) else None)
    return None

rows = ["# T7/T8 sweep comparison — baseline (adf9aea) vs new (HEAD)", "",
        "PYTHONHASHSEED=0, the eight sweep conditions. `-` = baseline only, `+` = new only; unchanged decisions are not listed.", ""]
for cond in CONDS:
    base, new = read(cond, "baseline"), read(cond, "new")
    db, dn = decisions(base), decisions(new)
    ib, inew = ir_lines(base), ir_lines(new)
    fd = first_diff(ib, inew)
    rows.append(f"## {cond}")
    rows.append("")
    metas_b = [d for d in db if d[1] == "meta"]; metas_n = [d for d in dn if d[1] == "meta"]
    fm = first_diff(metas_b, metas_n)
    rows.append(f"- first [meta] difference: " + (f"step {fm[1][0] if fm[1] else fm[2][0]}" if fm else "none"))
    if fd is None:
        rows.append(f"- [IR]/[IR-dist] lines: byte-identical ({len(ib)} lines)")
    elif fd[2] is None:
        rows.append(f"- [IR]/[IR-dist] lines: new is a prefix of baseline ({len(inew)} of {len(ib)} lines; "
                    f"the robot finishes earlier and stops observing)")
    else:
        sb = STEP.search(fd[1] or fd[2] or "").group(1)
        rows.append(f"- [IR]/[IR-dist] lines: identical up to step {int(sb)-1}, first difference at step {sb} "
                    f"(line {fd[0]} of {len(ib)} / {len(inew)})")
    rows.append(f"- run end: baseline {[d for d in db if d[1]=='meta'][-1][0]}, new {[d for d in dn if d[1]=='meta'][-1][0]} (last [meta] step)")
    rows.append("")
    sb, sn = set(db), set(dn)
    removed = [d for d in db if d not in sn]; added = [d for d in dn if d not in sb]
    if not removed and not added:
        rows.append("decision sequence unchanged."); rows.append(""); continue
    rows.append("```")
    for d in sorted(removed + added, key=lambda d: (d[0], d in added)):
        sign = "+" if d in added else "-"
        rows.append(f"{sign} step={d[0]:<4} {d[1]:<5} {d[2]}")
    rows.append("```"); rows.append("")
open(os.path.join(HERE, "summary.md"), "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
