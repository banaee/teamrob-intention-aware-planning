#!/usr/bin/env python3
"""
read5b.py — T-K part 1, step 5b, the planning set with context knowledge on (analysis/kitting/mpb/tk5b/README.md): the
set's reader. Reporting only; nothing here derives an expectation from a run.

The off side: analysis/kitting/mpb/<scenario>/on_single_task (the set's reference: context knowledge off, assignment
knowledge on, single_task); the on side: analysis/kitting/mpb/tk5b/<scenario>/on_single_task (context knowledge on).

    read5b.py expect     the preview before any run with context knowledge on: per scenario, the MPB chain
                         (analysis/instruments/mpb/chain.py) assembled from the oracle's per-tick table of each side
                         with the off run's own no_current_task ticks, terminal tick and horizon. The off line equals
                         the off run's chain (0 disagreements at HEAD). The on line is valid only up to the first tick
                         on which the on run's robot timing departs from off's (its own no_current_task ticks come only
                         from the run); holds and selections are not predicted.
    read5b.py report     per scenario, off against on, from the runs: the authored case (CASES, checked by the same
                         function on both sides), the decisions with their projection and hold, the admissions as the
                         meta-planner held them, the completion, the separation and the declared properties.

The authored case per scenario (analysis/kitting/mpb/README.md, REPORT.md "Per scenario: the decision it exposes",
coverage.md; the declared properties of properties.py where the scenario has them). A check returns (reached, where):
the same function reads both sides, so the off side, which reaches every case by the MPB's close-out, checks the check.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / "analysis" / "instruments" / "mpb"), str(ROOT / "analysis" / "instruments" / "common"),
                str(ROOT)]

from chain import assemble
from mpblib import load_ticks, load_decisions

VAR = "on_single_task"
OFF, ON = HERE.parent, HERE
SCENARIOS = ["scenario_s10_01", "scenario_s10_02", "scenario_s10_03", "scenario_s10_04", "scenario_s10_05",
             "scenario_s10_06", "scenario_s10_07", "scenario_s10_08", "scenario_s10_09", "scenario_s10_10",
             "scenario_s10_11", "scenario_s11_01", "scenario_s11_02", "scenario_s11_03", "scenario_s12_01",
             "scenario_s12_02"]


def short(key):
    if key is None:
        return "-"
    return key.split("(")[0] + ("(" + key.split("?item=")[1].split(")")[0].split(",")[0] + ")" if "?item=" in key else "")


def trig(d):
    t = d.trigger.value.replace("recognition_changed", "rc").replace("projection_expired", "pe")
    return t.replace("no_current_task", "nct") + (f"/{d.cause.value}" if d.cause else "")


def proj(d):
    if d.admitted is not None:
        return f"admitted {short(d.admitted.key)} [{','.join(d.warrant)}]"
    g = d.gate.value.removeprefix("none(").rstrip(")")
    fb = "none" if d.fallback is None else f"fallback {d.fallback.mode.value} k={d.fallback.k} end={d.fallback.end:.0f}"
    return f"{g} ({short(d.leader)}): {fb}"


def folder(sid, side):
    return (OFF if side == "off" else ON) / sid / VAR


# ---- the authored cases -------------------------------------------------------------------------------------------

class Run:
    def __init__(self, sid, side):
        d = folder(sid, side)
        self.dec = load_decisions(d / "actual_decisions.json")
        self.sel = {s["tick"]: s for s in json.load(open(d / "selection.json"))}
        self.robot = {r["tick"]: r for r in json.load(open(d / "robot.json"))}
        self.props = json.load(open(d / "properties.json"))
        self.prop = {p["name"]: p for p in self.props["properties"]}

    def hold(self, d):
        return self.sel[d.tick]["hold"] or 0

    def props_hold(self, *names):
        bad = [n for n in names if not self.prop[n]["holds"]]
        return (not bad, "; ".join(f"{n} {'holds' if self.prop[n]['holds'] else 'FAILS'}: {self.prop[n]['detail']}"
                                    for n in names))


def is_entered(d, item=None):
    return d.cause is not None and d.cause.value == "entered" and d.admitted is not None and \
        (item is None or item in d.admitted.key)


def c_admission_after_theta(r):
    """s10_01: the first admission (of item_1) is a recognition_changed (entered) after fallback decisions refused below
    θ, on commitment and observation."""
    i = next(i for i, d in enumerate(r.dec) if d.admitted is not None)
    d, before = r.dec[i], r.dec[:i]
    ok = (is_entered(d, "item_1") and before and all(b.gate.value == "none(below_theta)" and b.fallback for b in before)
          and set(d.warrant) == {"commitment", "observation"})
    return ok, f"{d.tick} {trig(d)}: {proj(d)}; before it {', '.join(str(b.tick) for b in before)}"


def c_props(*names):
    def f(r):
        return r.props_hold(*names)
    f.__doc__ = "the declared properties " + ", ".join(names)
    return f


def c_boundary_readmission(r):
    """s10_04: at the coffee break's boundary, replaced with the gate refusing for no observation on a fallback stand,
    and on the next tick entered, deliver_item(item_2) on commitment alone."""
    for a, b in zip(r.dec, r.dec[1:]):
        prev = next((x for x in reversed(r.dec[:r.dec.index(a)]) if x.admitted is not None), None)
        if (a.cause is not None and a.cause.value == "replaced" and a.gate.value == "none(leader_no_observation)"
                and a.fallback and a.fallback.mode.value == "standing" and prev is not None
                and prev.admitted.key.startswith("coffee_break") and b.tick == a.tick + 1 and is_entered(b, "item_2")
                and list(b.warrant) == ["commitment"]):
            return True, f"{a.tick} {trig(a)}: {proj(a)}; {b.tick} {trig(b)}: {proj(b)}"
    after = [x for x in r.dec if x.tick >= 120]
    return False, "after 120: " + "; ".join(f"{x.tick} {trig(x)}: {proj(x)}" for x in after[:3])


def c_lone_foreseeable(r):
    """s10_05: after the assigned tasks, coffee_break leads alone: a decision refused unwarranted on a fallback stand,
    then entered, coffee_break on observation alone."""
    a = next((x for x in r.dec if x.gate.value == "none(leader_unwarranted)" and x.leader.startswith("coffee_break")),
             None)
    b = next((x for x in r.dec if a is not None and x.tick > a.tick and is_entered(x, None)
              and x.admitted.key.startswith("coffee_break") and list(x.warrant) == ["observation"]), None)
    if a is None or b is None:
        return False, "no unwarranted refusal of coffee_break" if a is None else f"{a.tick} {trig(a)}: {proj(a)}; no entry"
    return True, f"{a.tick} {trig(a)}: {proj(a)}; {b.tick} {trig(b)}: {proj(b)}"


def c_sudden_stand(r):
    """s10_07: the retraction of item_1 in the carry on a fallback stand, the stand's doubling at a later expiry, and
    item_1 admitted again (entered) only later."""
    a = next((x for x in r.dec if x.cause is not None and x.cause.value == "retraction" and "item_1" in (x.leader or "")
              and x.fallback and x.fallback.mode.value == "standing"), None)
    if a is None:
        return False, "no retraction of item_1 on a stand"
    dbl = next((x for x in r.dec if x.tick > a.tick and x.trigger.value == "projection_expired" and x.fallback
                and x.fallback.mode.value == "standing" and x.fallback.k > a.fallback.k), None)
    re_ = next((x for x in r.dec if x.tick > a.tick and is_entered(x, "item_1")), None)
    ok = dbl is not None and re_ is not None
    return ok, (f"{a.tick} {trig(a)}: {proj(a)}; " + (f"{dbl.tick} {trig(dbl)}: {proj(dbl)}; " if dbl else "no doubling; ")
                + (f"{re_.tick} {trig(re_)}: {proj(re_)}" if re_ else "no re-admission"))


def c_change_of_mind(r):
    """s10_08: after item_1's admission, the human's change of mind is replaced through the coffee hypothesis, then
    deliver_item(item_2) entered."""
    i = next(i for i, d in enumerate(r.dec) if d.admitted is not None and "item_1" in d.admitted.key)
    nxt = next(d for d in r.dec[i + 1:] if d.trigger.value == "recognition_changed")
    ent = next((d for d in r.dec[i + 1:] if is_entered(d, "item_2")), None)
    ok = (nxt.cause.value == "replaced" and (nxt.leader or "").startswith("coffee_break") and ent is not None)
    return ok, f"{nxt.tick} {trig(nxt)}: {proj(nxt)}; " + (f"{ent.tick} {trig(ent)}: {proj(ent)}" if ent else "no entry")


def c_misdelivery(r):
    """s10_09: the retraction of item_1 (inadequate) on a moving fallback cut at an object, the unexplained finding
    outliving a re-decision (X5's ground (1), measured)."""
    a = next((x for x in r.dec if x.cause is not None and x.cause.value == "retraction" and "item_1" in (x.leader or "")),
             None)
    x5 = r.props["measures"].get("x5_ground1") or []
    cut = a is not None and a.fallback is not None and a.fallback.mode.value == "moving" and a.fallback.duration < a.fallback.k
    ok = a is not None and a.gate.value == "none(leader_inadequate)" and cut and bool(x5)
    return ok, ((f"{a.tick} {trig(a)}: {proj(a)}, duration {a.fallback.duration:.2f} < k" if a else "no retraction")
                + f"; X5 ground (1): {x5 or 'none'}")


def c_boundary_cause(r):
    """s10_11: a recognition_changed with the cause boundary."""
    a = next((x for x in r.dec if x.cause is not None and x.cause.value == "boundary"), None)
    return a is not None, (f"{a.tick} {trig(a)}: {proj(a)}" if a else "none")


def c_walker_stander(r):
    """s11_02: the walk's moving fallback cut (at door_N) with a positive hold; the stand's doubling expiries with
    holds (TODO-132 (a)'s evidence)."""
    cut = next((x for x in r.dec if x.fallback and x.fallback.mode.value == "moving" and x.fallback.duration < x.fallback.k
                and r.hold(x) > 0), None)
    t = r.props["measures"].get("todo132a") or {}
    stand = [(x[0], x[4]) for x in t.get("decisions", [])]
    ok = cut is not None and len(stand) >= 2
    return ok, ((f"cut {cut.tick} {trig(cut)}: {proj(cut)}, hold {r.hold(cut)}" if cut else "no held cut fallback")
                + f"; the stand's decisions (tick, hold): {stand}; past the break: {t.get('holds_past_break')}")


CASES = {
    "scenario_s10_01": ("admission after θ", c_admission_after_theta),
    "scenario_s10_02": ("the hold against the admitted walk (C1, D4)", c_props("P2a", "P2b")),
    "scenario_s10_03": ("retention through the mid-action change, then the retraction (A5)", c_props("P3a", "P3b", "P3c")),
    "scenario_s10_04": ("boundary re-admission on commitment (B2, B5)", c_boundary_readmission),
    "scenario_s10_05": ("the lone foreseeable hypothesis (B4)", c_lone_foreseeable),
    "scenario_s10_06": ("the control (no hold, the reference's completion and positions)", c_props("P8a", "P8b", "P8c")),
    "scenario_s10_07": ("the sudden stand mid-carry", c_sudden_stand),
    "scenario_s10_08": ("the change of mind, replaced through coffee_break", c_change_of_mind),
    "scenario_s10_09": ("the misdelivery (B3, C4, E11)", c_misdelivery),
    "scenario_s10_10": ("a record kept through a dip below θ (E6)", c_props("P10.10")),
    "scenario_s10_11": ("the cause boundary (A4)", c_boundary_cause),
    "scenario_s11_01": ("the occupied target: the switch at an expiry (C7, D7)", c_props("P6.1", "P6.2")),
    "scenario_s11_02": ("walker and stander (C5, D5, D6, E5, E12)", c_walker_stander),
    "scenario_s11_03": ("the switch while carrying (D9)", c_props("P11.3a", "P11.3b", "P11.3c")),
    "scenario_s12_01": ("the switch against an admitted projection (D8)", c_props("P12.1a", "P12.1b")),
    "scenario_s12_02": ("the hold against the admitted wait at the coffee machine (C2)", c_props("P12.2a", "P12.2b", "P12.2c")),
}


# ---- the two readings ---------------------------------------------------------------------------------------------

def expect():
    print("| scenario | side | the chain from the oracle's table with the off run's no_current_task ticks "
          "(tick trigger/cause: projection) |")
    print("|---|---|---|")
    for sid in SCENARIOS:
        obs = json.load(open(folder(sid, "off") / "observed.json"))
        for side in ("off", "on"):
            ch = assemble(load_ticks(folder(sid, side) / "expected_ticks.json"), set(obs["no_current_task"]),
                          obs["terminal"], obs["horizon"])
            print(f"| {sid} | {side}{' (preview)' if side == 'on' else ''} | "
                  f"{'; '.join(f'{d.tick} {trig(d)}: {proj(d)}' for d in ch)} |")


def held(decisions, terminal):
    """The admissions as the meta-planner held them: from a decision that admits to the tick before the next decision;
    the terminal decision holds nothing for a plan."""
    out = []
    decisions = [d for d in decisions if terminal is None or d.tick < terminal]
    for i, d in enumerate(decisions):
        if d.admitted is None:
            continue
        end = decisions[i + 1].tick - 1 if i + 1 < len(decisions) else (terminal - 1 if terminal else "end")
        out.append(f"{short(d.admitted.key)} {d.tick}-{end}")
    return out


def rows():
    """The coverage rows whose instances the prior moves, over the sixteen runs per side (coverage.md's definitions):
    A4 the cause boundary; A7 a no_current_task decision on a tick at or after the recorded fallback's end; A8 a
    recognition_changed decision on such a tick; B11 replaced with the gate clearing on the same tick; a switch (the
    winner other than the task the robot held, that task not completed), with the robot's state on the tick before
    (carrying: D9; otherwise walking: D7 or D8 by the projection), the held task still in the pool (a decision after
    the robot's own release is a new selection); E6 the record kept through a tick below θ (the
    oracle's table: the recorded hypothesis leads with the gate refusing below θ, no decision on the tick)."""
    out = {}
    for side in ("off", "on"):
        found = {k: [] for k in ("A4", "A7", "A8", "B11", "switch", "E6")}
        for sid in SCENARIOS:
            r, s = Run(sid, side), sid.removeprefix("scenario_")
            ticks = {t.tick: t for t in load_ticks(folder(sid, side) / "expected_ticks.json")}
            expiry, record, held_task = None, None, None
            dec = {d.tick: d for d in r.dec}
            end = r.props["terminal"] if r.props["terminal"] is not None else max(ticks) + 1
            for t in range(0, end):                       # C6: nothing is evaluated after the terminal decision
                d = dec.get(t)
                if d is None:
                    row = ticks.get(t)
                    if record is not None and row is not None and row.leader == record and row.gate.value == "none(below_theta)":
                        found["E6"].append(f"{s} {t}")
                    continue
                if d.cause is not None and d.cause.value == "boundary":
                    found["A4"].append(f"{s} {t}")
                if expiry is not None and t >= expiry and d.trigger.value == "no_current_task":
                    found["A7"].append(f"{s} {t}")
                if expiry is not None and t >= expiry and d.trigger.value == "recognition_changed":
                    found["A8"].append(f"{s} {t}")
                if d.cause is not None and d.cause.value == "replaced" and d.admitted is not None:
                    found["B11"].append(f"{s} {t}")
                win = r.sel[t]["winner"]
                pool = [c["task"] for c in r.sel[t]["candidates"]]
                if held_task is not None and win is not None and win != held_task and held_task in pool \
                        and d.trigger.value != "no_current_task":
                    state = "carrying" if (r.robot.get(t - 1) or {}).get("carrying") else "walking"
                    found["switch"].append(f"{s} {t} ({state}, {'admitted' if d.admitted else 'fallback'})")
                held_task = win
                expiry = d.fallback.end if d.admitted is None and d.fallback is not None else None
                record = d.leader if d.admitted is not None else None
        out[side] = found
    print("| row | off | on |")
    print("|---|---|---|")
    for k in ("A4", "A7", "A8", "B11", "switch", "E6"):
        print(f"| {k} | {'; '.join(out['off'][k]) or 'none'} | {'; '.join(out['on'][k]) or 'none'} |")


def report():
    print("### The authored case, off against on\n")
    print("| scenario | the authored case | off | on | on: where |")
    print("|---|---|---|---|---|")
    for sid in SCENARIOS:
        name, f = CASES[sid]
        (a, _), (b, wb) = f(Run(sid, "off")), f(Run(sid, "on"))
        print(f"| {sid} | {name} | {'reached' if a else 'NOT reached'} | {'reached' if b else 'NOT reached'} | {wb} |")
    print("\n### Completion and separation, off against on\n")
    print("| scenario | completion off | on | holds off (tick, ticks) | on | min separation off (tick) | on | "
          "F1 viol/stand/recede off | on | properties off | on |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for sid in SCENARIOS:
        r = {s: Run(sid, s) for s in ("off", "on")}
        m = {s: r[s].props["measures"] for s in r}
        f1 = {s: "/".join(str(m[s]["f1"][k]) for k in ("viol", "stand", "recede")) for s in r}
        ps = {s: ", ".join(f"{p['name']} {'yes' if p['holds'] else 'NO'}" for p in r[s].props["properties"]) or "-"
              for s in r}
        hs = {s: ", ".join(f"({a}, {b})" for a, b in m[s]["holds"]) or "none" for s in r}
        sep = {s: f"{m[s]['sep_min_continuous'][0]:.1f} ({m[s]['sep_min_continuous'][1]})" for s in r}
        print(f"| {sid} | {r['off'].props['completion']} | {r['on'].props['completion']} | {hs['off']} | {hs['on']} | "
              f"{sep['off']} | {sep['on']} | {f1['off']} | {f1['on']} | {ps['off']} | {ps['on']} |")
    print("\n### The decisions, off against on\n")
    print("| scenario | side | decisions (tick trigger/cause: projection, hold) | held admissions |")
    print("|---|---|---|---|")
    for sid in SCENARIOS:
        for side in ("off", "on"):
            r = Run(sid, side)
            cells = [f"{d.tick} {trig(d)}: {proj(d)}, {r.hold(d)}" for d in r.dec]
            print(f"| {sid} | {side} | {'; '.join(cells)} | {', '.join(held(r.dec, r.props['terminal'])) or 'none'} |")


if __name__ == "__main__":
    {"expect": expect, "report": report, "rows": rows}[sys.argv[1]]()
