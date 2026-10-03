#!/usr/bin/env python3
"""
L. The lifecycle's events per run, POST (L-build) against PRE (IRB.2b), prior on first, then prior off, then the four
supplementary runs:
  boundaries   every [IR-boundary] tick, with the action it names and whether a pin ([IR-complete]) falls on the same
               tick ("pin" / "NO PIN": T-D L1's new boundaries); PRE's boundary ticks beside them;
  re-entries   every [IR-reentry] (tick, key) (L4);
  pins         every [IR-complete] (tick, key), a key pinned more than once marked;
  retractions  every [meta-trig] with cause=retraction (L2 (ii)), with the [meta-proj] answer of that tick;
  boundary fires  every [meta-trig] with cause=boundary (L5 B), with its [meta-proj] answer;
  causes       the count of recognition_changed per cause (entered, replaced, boundary, retraction), and PRE's total.
Run from this directory: ~/python-envs/ir-nomesa-env/bin/python l_events.py > l_events.txt
"""
import re
from tdlib import runs, parse, label


def proj_after(path):
    """step -> the [meta-proj] projection= answer that follows that step's [meta-trig]."""
    out, step = {}, None
    for l in open(path, errors="replace"):
        if l.startswith("[meta-trig]"):
            step = int(re.match(r"\[meta-trig\] step=(\d+)", l)[1])
        elif l.startswith("[meta-proj]") and step is not None:
            out[step] = re.search(r"projection=(\S+)", l)[1]
    return out


def events(r):
    post, pre = parse(r["post"]), parse(r["pre"])
    pin_ticks = {s for s, _ in post["pins"]}
    bounds = [f"{b} {post['boundary_action'].get(b)} {'pin' if b in pin_ticks else 'NO PIN'}" for b in post["boundary"]]
    counts = {}
    for _, trig, cause in post["triggers"]:
        if trig == "recognition_changed":
            counts[cause] = counts.get(cause, 0) + 1
    pre_rc = sum(1 for _, trig, _ in pre["triggers"] if trig == "recognition_changed")
    proj = proj_after(r["post"])
    retr = [f"{s} -> {proj.get(s)}" for s, trig, c in post["triggers"] if c == "retraction"]
    bfire = [f"{s} -> {proj.get(s)}" for s, trig, c in post["triggers"] if c == "boundary"]
    keys = [k for _, k in post["pins"]]
    pins = [f"{s} {k}{' (again)' if keys[:i].count(k) else ''}" for i, (s, k) in enumerate(post["pins"])]
    return dict(bounds=bounds, pre_bounds=pre["boundary"], reent=[f"{s} {k}" for s, k in post["reentries"]],
                pins=pins, retr=retr, bfire=bfire, counts=counts, pre_rc=pre_rc)


def main():
    print(__doc__)
    rs = runs()
    groups = [("prior on (primary)", [r for r in rs if r["prior"] == "on"]),
              ("prior off (appendix)", [r for r in rs if r["prior"] == "off"]),
              ("supplementary (wrong table)", runs(supp=True))]
    tot = {}
    for title, group in groups:
        print(f"\n# {title}")
        for r in group:
            e = events(r)
            print(f"\n## {r['set']}/{r['name']}  [{label(r)}]")
            print(f"  boundaries  {'; '.join(e['bounds']) or '-'}")
            print(f"     (PRE)    {', '.join(map(str, e['pre_bounds'])) or '-'}")
            print(f"  re-entries  {'; '.join(e['reent']) or '-'}")
            print(f"  pins        {'; '.join(e['pins']) or '-'}")
            print(f"  retractions {'; '.join(e['retr']) or '-'}")
            print(f"  boundary fires {'; '.join(e['bfire']) or '-'}")
            c = e["counts"]
            print(f"  recognition_changed: entered {c.get('entered', 0)}, replaced {c.get('replaced', 0)}, boundary "
                  f"{c.get('boundary', 0)}, retraction {c.get('retraction', 0)} (PRE total {e['pre_rc']})")
            t = tot.setdefault(title, dict(nopin=0, reent=0, retr=0, bfire=0))
            t["nopin"] += sum(b.endswith("NO PIN") for b in e["bounds"])
            t["reent"] += len(e["reent"]); t["retr"] += len(e["retr"]); t["bfire"] += len(e["bfire"])
    print("\n# totals (runs not grouped)")
    for title, t in tot.items():
        print(f"  {title}: boundaries without a pin {t['nopin']}, re-entries {t['reent']}, retractions {t['retr']}, "
              f"boundary fires {t['bfire']}")


if __name__ == "__main__":
    main()
