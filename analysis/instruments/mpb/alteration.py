#!/usr/bin/env python3
"""
alteration.py — the meta-planner test-bed's single-rule alteration test (the engine and the rules every domain shares;
a domain's own rules and its call are analysis/<domain>/mpb/alteration.py, since dock_loading's MPB, 2 October 2026) (MPB-4; the IRB's method, its REPORT.md,
"The instrument can fail"): one rule of the derivation altered at a time in a scratch copy of the instrument's sources
(analysis/instruments/mpb and analysis/instruments/irb, never committed), the per-tick table and the chain re-derived from each
scenario's committed trajectory and observed run facts, and compared against the unchanged actual files. The count of
disagreements per scenario shows whether the comparison detects the alteration. An undetected alteration is recorded
as a property of the test set with its reason, unless it is an oracle defect.

    analysis/<domain>/mpb/alteration.py <scratch dir> <scenario dir> [<scenario dir> ...]
                                                            (each: analysis/<domain>/mpb/<scenario>/on_single_task)

The shared alterations: the expiry cadence (A1 to A5), the projection's identity (B2, B3), the gate with warrant (C2,
C3; C1, commitment warrant ignored, retired in the gate rulings' build: AM67 made it the rule); and two of the chain's
retention rules (D1, D2). RANK (C4 to C6, the gate rulings' build): the evidence rank, run on step 5's planning cases
only (D6). B1 (the method guards) names a domain's schemas and is the
domain's. The scratch copies of both oracles read the repository's root (ROOT) for the domain's files: the IR oracle's
own ROOT is patched as the MPB oracle's is (a defect of the copy since the IR oracle reads the layout's areas, T-G A9;
found when dock_loading's MPB was built, the table unchanged).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = sys.executable

SHARED = [
    ("A1", "the fallback's end without the observation offset", "mpb/mpb_oracle.py",
     ["OBSERVATION_OFFSET = 1.0"], ["OBSERVATION_OFFSET = 0.0"]),
    ("A2", "the run length by exact direction equality (no 1e-9 resolution)", "mpb/mpblib.py",
     ["DIRECTION_RESOLUTION = 1e-9"], ["DIRECTION_RESOLUTION = 0.0"]),
    ("A3", "a turn resets the run length to 0", "mpb/mpblib.py",
     ["<= DIRECTION_RESOLUTION else 1"], ["<= DIRECTION_RESOLUTION else 0"]),
    ("A4", "landmarks not counted as fixed objects for the ray", "mpb/mpb_oracle.py",
     ['{o["id"]: tuple(o["position"]) for o in layout["env_objects"]}'],
     ['{o["id"]: tuple(o["position"]) for o in layout["env_objects"] if o["type"] != "landmark"}']),
    ("A5", "projection_expired asked before recognition_changed on a shared tick", "mpb/chain.py",
     ["            if cause is not None:\n                trigger = Trigger.RECOGNITION_CHANGED\n"
      "            elif expiry is not None and t >= expiry:                          # C4\n"
      "                trigger = Trigger.PROJECTION_EXPIRED\n"],
     ["            if expiry is not None and t >= expiry:\n"
      "                trigger, cause = Trigger.PROJECTION_EXPIRED, None\n"
      "            elif cause is not None:\n                trigger = Trigger.RECOGNITION_CHANGED\n"]),
    ("B2", "the ray does not skip an object whose radius contains its start", "mpb/mpblib.py",
     ["            continue                                   # the start inside its radius: skipped\n"],
     ["            pass\n"]),
    ("B3", "the moving fallback not cut at the wall or the first object", "mpb/mpblib.py",
     ["duration = min(float(p.run_length), reach(position, u, room) / length)"],
     ["duration = float(p.run_length)"]),
    ("C2", "the movement source loosened to any walked path since the origin", "irb/oracle.py",
     ['return "observation" if math.dist(self.origin[k][0], g) - math.dist(pos, g) > 0 else "none"'],
     ['return "observation" if self.odo - self.origin[k][1] > 0 else "none"']),
    ("C3", "warrant asked before the leader's adequacy", "irb/oracle.py",
     ['        if adequacy == "inadequate":\n            return "none(leader_inadequate)"\n'
      '        if adequacy != "adequate":\n            return "none(leader_no_observation)"\n'
      '        if warrant != "observation":\n'
      '            return "none(leader_unwarranted)"\n'],
     ['        if warrant != "observation":\n'
      '            return "none(leader_unwarranted)"\n'
      '        if adequacy == "inadequate":\n            return "none(leader_inadequate)"\n'
      '        if adequacy != "adequate":\n            return "none(leader_no_observation)"\n']),
    ("D1", "no retraction (the recorded hypothesis's inadequacy fires nothing)", "mpb/chain.py",
     ['elif row.adequacy.get(recorded) == "inadequate":'], ["elif False:"]),
    ("D2", "boundary asked before replaced", "mpb/chain.py",
     ["                if row.leader != recorded:\n                    cause = Cause.REPLACED\n"
      "                elif row.boundary:\n                    cause = Cause.BOUNDARY\n"],
     ["                if row.boundary:\n                    cause = Cause.BOUNDARY\n"
      "                elif row.leader != recorded:\n                    cause = Cause.REPLACED\n"]),
]

# The rank alterations (the gate rulings' build, D6): run on step 5's six scenarios only (context knowledge on). With
# context knowledge off the leader is never outranked (the belief is the evidence), so on the planning set's sixteen
# they cannot be detected by construction, a property of that set, and they are not run there.
RANK = [
    ("C4", "the outranked condition not asked", "irb/oracle.py",
     ['        if rank == "outranked":\n            return "none(leader_outranked)"\n'], ['']),
    ("C5", "a tie refused (a key within the agreement level of another counted outranked)", "irb/oracle.py",
     ['    if any(math.isclose(v, E[k], **AGREEMENT) for v in others):\n        return UNDETERMINED\n'],
     ['    if any(math.isclose(v, E[k], **AGREEMENT) for v in others):\n        return "outranked"\n']),
    ("C6", "the rank read from the belief instead of the evidence", "irb/oracle.py",
     ['orc.warrant(k, pos, world), rank(E, k))'], ['orc.warrant(k, pos, world), rank(B, k))']),
]


def prepare(scratch: Path, label: str, target: str, old, new) -> Path:
    base = scratch / label
    if base.exists():
        shutil.rmtree(base)
    (base / "analysis" / "instruments").mkdir(parents=True)
    for sub in ("mpb", "irb"):
        shutil.copytree(ROOT / "analysis" / "instruments" / sub, base / "analysis" / "instruments" / sub,
                        ignore=shutil.ignore_patterns("scenario_*", "runs", "__pycache__", "*.png"))
    path = base / "analysis" / "instruments" / target
    text = path.read_text()
    for o, n in zip(old, new):
        assert text.count(o) == 1, f"{label}: the altered text is not found exactly once in {target}"
        text = text.replace(o, n)
    path.write_text(text)
    return base


def rederive(base: Path, scen: Path, work: Path, domain: str):
    """The per-tick table and the chain from the scratch sources; the actual files copied unchanged; the compare."""
    work.mkdir(parents=True, exist_ok=True)
    for f in ("actual_ticks.json", "actual_decisions.json", "actual_log_decisions.json", "observed.json"):
        shutil.copy(scen / f, work / f)
    # the run file: configs/<domain>/mpb/ or a set's folder below it (step 5's tk/, since the gate rulings' build)
    run_file = min((ROOT / "configs" / domain / "mpb").rglob(f"{scen.parent.name}.yaml"), key=lambda p: len(p.parts))
    log = next((scen.parents[1] / "runs").glob(f"*_{scen.parent.name}_{scen.name}.log"))
    env = dict(PYTHONHASHSEED="0", PATH="/usr/bin:/bin", PYTHONPATH=str(ROOT))
    oracle = base / "analysis" / "instruments" / "mpb" / "mpb_oracle.py"
    # the scratch oracle's ROOT is the repo's (its sys.path), but the IR oracle it imports must be the scratch copy
    src = oracle.read_text().replace('ROOT = Path(__file__).resolve().parents[3]', f'ROOT = Path("{ROOT}")') \
        .replace('str(ROOT / "analysis" / "instruments" / "irb")',
                 f'"{base / "analysis" / "instruments" / "irb"}"')
    oracle.write_text(src)
    ir = base / "analysis" / "instruments" / "irb" / "oracle.py"
    ir.write_text(ir.read_text().replace('ROOT = Path(__file__).resolve().parents[3]', f'ROOT = Path("{ROOT}")'))
    subprocess.run([PY, str(oracle), str(scen / "trajectory.json"), str(run_file), str(log),
                    str(work / "expected_ticks.json")], check=True, env=env, cwd=ROOT, capture_output=True)
    subprocess.run([PY, str(base / "analysis" / "instruments" / "mpb" / "chain.py"), str(work / "expected_ticks.json"),
                    str(work / "observed.json"), str(work / "expected_decisions.json")], check=True, env=env,
                   capture_output=True)
    subprocess.run([PY, str(base / "analysis" / "instruments" / "mpb" / "compare.py"), scen.parent.name, str(work)], check=True,
                   env=env, capture_output=True)
    return len(json.load(open(work / "diff.json"))["disagreements"])


def main(domain, alterations):
    """Every alteration over the scenario folders of argv[2:], in the order given; prints the table."""
    scratch = Path(sys.argv[1])
    scens = [Path(p).resolve() for p in sys.argv[2:]]
    rows = []
    for label, text, target, old, new in alterations:
        base = prepare(scratch, label, target, old, new)
        counts = [rederive(base, s, scratch / label / "work" / s.parent.name, domain) for s in scens]
        rows.append((label, text, counts))
        print(f"{label} {text}: " + " / ".join(map(str, counts)), flush=True)
    print("\n| alteration | " + " | ".join(s.parent.name for s in scens) + " |")
    print("|---|" + "---|" * len(scens))
    for label, text, counts in rows:
        print(f"| {label}: {text} | " + " | ".join(map(str, counts)) + " |")
