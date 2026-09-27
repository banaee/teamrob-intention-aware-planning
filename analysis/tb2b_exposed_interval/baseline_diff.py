#!/usr/bin/env python3
"""
baseline_diff.py — TB.2b's regeneration criterion (the cognitive-loop correction; design_decisions.md, "The cognitive
loop does not end with the task pool", its consequences as refined in TB.2b records).

Per log, PRE (the 1.5c baselines, copied to pre/<set>/ before the build) against POST (the regenerated
analysis/<set>/sweep/), and the four supplementary runs (pre/supp/ against post/supp/):
  (i)   the log with every [IR*] line removed is byte-identical;
  (ii)  the [IR*] lines up to and including the declared completion tick N (the PRE log's
        `[meta] step=N all tasks complete`; every tick when the robot never completes) are byte-identical, [IR-prior]
        (no step) included;
  (iii) the .rec stream is byte-identical;
and every POST [IR*] line beyond (ii) carries a step > N. A failure prints its first differing line. Then per log the
number of new [IR*] lines by kind and the exposed interval N+1..last.
"""
import re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SETS = ["tb1a_destination", "tb1b_two_tables", "tb1c_realized_flip", "tb3_full_reorder"]
STEP = re.compile(r"step=(\d+)")
DONE = re.compile(r"^\[meta\] step=(\d+) all tasks complete")


def pairs():
    for s in SETS:
        for post in sorted((ROOT / "analysis" / s / "sweep").glob("*.log")):
            yield s, HERE / "pre" / s / post.name, post
    for post in sorted((HERE / "post" / "supp").glob("*.log")):
        yield "supp", HERE / "pre" / "supp" / post.name, post


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f"line {i + 1}: PRE {x.rstrip()!r} | POST {y.rstrip()!r}"
    return f"length PRE {len(a)} POST {len(b)}"


def is_ir(line):
    return line.startswith("[IR")


def step_of(line):
    m = STEP.search(line)
    return int(m[1]) if m else None


def check(pre, post):
    a, b = pre.read_text().splitlines(True), post.read_text().splitlines(True)
    fails = []
    na, nb = [l for l in a if not is_ir(l)], [l for l in b if not is_ir(l)]
    if na != nb:
        fails.append("(i) " + first_diff(na, nb))
    done = next((int(DONE.match(l)[1]) for l in a if DONE.match(l)), None)
    ia = [l for l in a if is_ir(l)]
    ib = [l for l in b if is_ir(l)]
    upto = [l for l in ib if done is None or step_of(l) is None or step_of(l) <= done]
    if ia != upto:
        fails.append("(ii) " + first_diff(ia, upto))
    rest = ib[len(upto):] if ib[:len(upto)] == upto else [l for l in ib if l not in upto]
    if any(step_of(l) is None or (done is not None and step_of(l) <= done) for l in rest):
        fails.append("(ii) a new [IR*] line at or before the declared tick")
    if pre.with_suffix(".rec").read_bytes() != post.with_suffix(".rec").read_bytes():
        fails.append("(iii) .rec differs")
    kinds = Counter(l.split("]")[0] + "]" for l in rest)
    steps = [step_of(l) for l in rest]
    return fails, done, kinds, (min(steps), max(steps)) if steps else None


def main():
    nfail = 0
    print(f"{'set/log':62} {'N':>4} {'exposed':>9}  new [IR*] lines by kind  criterion")
    for s, pre, post in pairs():
        fails, done, kinds, span = check(pre, post)
        nfail += bool(fails)
        span_s = f"{span[0]}-{span[1]}" if span else "-"
        kind_s = " ".join(f"{k}={v}" for k, v in sorted(kinds.items()))
        print(f"{s + '/' + post.stem:62} {done if done is not None else '-':>4} {span_s:>9}  {kind_s:44} "
              f"{'MET' if not fails else 'FAILED'}")
        for f in fails:
            print(f"    {f}")
    print(f"\n{nfail} log(s) fail the criterion")
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
