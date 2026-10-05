#!/usr/bin/env python3
"""
mpb_oracle.py — the meta-planner test-bed's per-tick table of parts 1 to 3 (MPB-1; design_decisions.md, "The meta-planner
test-bed (MPB)"), derived before the run from the human's side alone: the trajectory (analysis/irb/
trajectory.py, the load-time replay expanded per tick with the body's timing, its own process) and the records.

    mpb_oracle.py <trajectory.json> <run file> <run.log | theta=<value>> <expected_ticks.json>

Prior on only: the IRB's oracle derives the support under the prior (its rule 1), and MPB-6 compares no
prior-off run against the oracle.

Since the gate rulings' build (stage 4): the gate as the IRB's oracle now derives it (no commitment warrant, AM67; the
outranked refusal last, AM68, D1; undetermined where its own evidence cannot decide the rank, D3), so the admission's
warrant source is observation alone.
Per tick: the leader, the boundary, the adequacy finding, every live hypothesis's hypothesis adequacy and the gate's
outcome (the IRB's oracle, analysis/irb/oracle.py, its rules 1 to 23 with their sources, imported unchanged); the
leader's warrant sources when the gate clears; P4's perception facts and the fallback projection a decision on the
tick would rest on (mpblib); and, when the gate clears, the admitted projection's identity: the leader's key and the
planner's decomposition of its task in the tick's world (the domain's structure, as the IRB uses it; not cost,
realization or selection).
Beside the table, for the figure only (plot_ir.py; never compared): per tick the belief and the tail probability S of
every hypothesis of the support and the lifecycle, the IRB's oracle rows as they are (the belief carries the
output floor of the setup's robot items, held outside the support).

The independence boundary (MPB-1): this process imports nothing from shared/meta_planner.py, shared/realization.py,
shared/projection.py, shared/recognizer.py, shared/likelihood_functions.py or mesa_sim/ (RobotAgent._perceive), nor
world/human_executor.py (which imports shared/projection.py), and asserts at exit that none was loaded. θ is read from
the run's [run] header, the one value read from the log (as the IRB's oracle reads it).

T-F part 1 (design_records.md, "T-F part 1: the conditions human-unaware and intention-unaware", R9 as amended by A,
THE PLAN APPROVED, A TO G): the run file's condition, read by R5 (conditions.py, the instrument's own reading), decides
the table. Intention-aware: as above. Intention-unaware: no recognition columns; the gate refuses on every tick with
none(intention_off); P4's perception and the fallback per tick (the oracle checks the decisions and the fallback
projections only). Human-unaware: admission refuses with none(no_human) before the gate (R7, E); no perception, no
fallback, no recognition.

Sources: MPB = design_decisions.md "The meta-planner test-bed (MPB)"; DG = "T-D G: admission" (AD1, AD4); DP = "T-D P"
(P4, Q6); IO = shared/io_contracts.md §2.2; IR = analysis/irb/README.md (its rules 1 to 23).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "analysis" / "instruments" / "irb"), str(Path(__file__).resolve().parent)]

import yaml
import oracle as ir                                    # the IRB's oracle (analysis/irb/oracle.py)
from shared.knowledge import TaskModel
from shared.planner import AdaptivePlanner, DecompositionError
from mpblib import Action, Admitted, Gate, Room, TickRow, dump, fallback, perception
from conditions import Condition, effective, stated

FORBIDDEN = ("shared.meta_planner", "shared.realization", "shared.projection", "shared.recognizer",
             "shared.likelihood_functions", "world.human_executor")

# IO / DP P4: the human projection, the fallback included, starts at the observation offset: the observed position is
# true at step 1 of the robot's projection (L2 of the Phase 4 records; docs/assumptions.md 5.1).
OBSERVATION_OFFSET = 1.0


def room(traj, run_file) -> Room:
    """DP P2 / P4: the workspace rectangle (the layout's space, centred) and every non-portable object of the layout,
    landmarks included; the arrival radius the body's (the trajectory's parameters)."""
    cfg = yaml.safe_load(open(run_file))
    domain_config = ir.domain_of(run_file)                       # the run file's domain (since the sort)
    sc = domain_config["scenarios"][cfg["scenario"]]
    layout = json.load(open(ROOT / domain_config["layouts"][cfg.get("layout") or sc.reference_layouts[0]]))
    w, h = layout["space"]["width"], layout["space"]["height"]
    return Room(-w / 2, w / 2, -h / 2, h / 2, {o["id"]: tuple(o["position"]) for o in layout["env_objects"]},
                traj["params"]["proximity"])


def unaware_rows(traj, rm: Room, condition: Condition):
    """The table of a run in which the recognizer computes nothing (T-F part 1, A): intention-unaware, the gate's
    refusal none(intention_off) on every tick (R6), the human observed, so P4's perception and the fallback a decision
    on the tick would rest on; human-unaware, admission's none(no_human) before the gate (R7, E), no observed human, so
    no perception and no fallback. No leader, boundary, finding, adequacy or warrant: no recognition."""
    positions = [(r["x"], r["y"]) for r in traj["rows"]]                          # tick -1 first
    perc = perception(positions)
    out = []
    for i, trow in enumerate(traj["rows"]):
        t = trow["tick"]
        if t < 0:
            continue
        if condition is Condition.HUMAN_UNAWARE:
            out.append(TickRow(t, None, False, None, Gate.NO_HUMAN, {}, {}, (), None, None, None))
        else:
            out.append(TickRow(t, None, False, None, Gate.INTENTION_OFF, {}, {}, (), perc[i],
                               fallback(t, (trow["x"], trow["y"]), perc[i], rm, OBSERVATION_OFFSET), None))
    return out


class OutsidePreRunDomain(Exception):
    """The scenario's per-tick table is not derivable before the run (MPB-3)."""


def derive(traj, run_file, alpha, theta):
    domain_config = ir.domain_of(run_file)                       # the run file's domain (since the sort)
    human = next(a for a in domain_config["scenarios"][traj["scenario"]].agents if a.agent_type == "human")
    condition = effective(stated(run_file)).condition                             # T-F part 1, R5
    if condition is not Condition.INTENTION_AWARE:
        return unaware_rows(traj, room(traj, run_file), condition)
    # IO §2.1, the recognizer's constructor (assigned_tasks): None or [] switches the support restriction off. With it off every
    # hypothesis is admissible, the robot's own items' deliveries included, so the robot's acts change human-side
    # hypothesis state and the table is not derivable before the run (MPB-3, MPB-6). Found in part (iii): the IR
    # oracle's support rule (its rule 1) assumes a non-empty assignment (class 1, REPORT.md).
    if not human.assigned_tasks:
        raise OutsidePreRunDomain(f"{traj['scenario']}: the human has no assigned tasks, so the support restriction is "
                                  f"off (shared/io_contracts.md: None or [] switches it off); MPB-3's pre-run "
                                  f"independence does not hold")
    context = bool(yaml.safe_load(open(run_file))["context_knowledge"])          # T-K part 1 (stage 6)
    rows, _, _ = ir.run(traj, alpha, theta, domain_config, context)
    agent = human.agent_id
    task_model = TaskModel(domain_config["register_fn"](), domain_config["task_model"])
    areas = ir.areas_of(domain_config, traj["layout"])
    planner = AdaptivePlanner(knowledge=task_model)
    space = ir.hypothesis_space(task_model, traj["types"])
    rm = room(traj, run_file)
    positions = [(r["x"], r["y"]) for r in traj["rows"]]                          # tick -1 first
    perc = perception(positions)
    traj_row = {r["tick"]: r for r in traj["rows"]}
    per_tick = {}
    for r in rows:
        per_tick.setdefault(r["tick"], []).append(r)
    out = []
    for i, trow in enumerate(traj["rows"]):
        t = trow["tick"]
        if t < 0:
            continue
        hyps = per_tick[t]
        head = hyps[0]
        leader = head["most_likely"] or None
        gate = Gate(head["gate"])
        adequacy = {h["key"]: h["adequacy"] for h in hyps if h.get("key")}
        ow = {h["key"]: h["warrant"] for h in hyps if h.get("key")}
        warrant, admitted = (), None
        if gate is Gate.CLEARS:
            warrant = ("observation",)            # DG AD4: the admission's source; observation only since AM67 (D2)
            world = ir.world_of(traj_row[t], traj, agent, areas)
            try:
                actions = planner.decompose(space[leader], agent, world)
            except DecompositionError:
                actions = None
            if actions is not None:
                admitted = Admitted(leader, tuple(Action(a.action_name, tuple(sorted(a.bindings.items())))
                                                  for a in actions))
        pos = (trow["x"], trow["y"])
        out.append(TickRow(t, leader, bool(head["boundary"]), head["finding"] or None, gate, adequacy, ow, warrant, perc[i],
                           fallback(t, pos, perc[i], rm, OBSERVATION_OFFSET), admitted))
    return out


if __name__ == "__main__":
    traj = json.load(open(sys.argv[1]))
    run_file = sys.argv[2]
    alpha = float(yaml.safe_load(open(run_file))["test_level"])
    if sys.argv[3].startswith("theta="):        # the expectations before any run: theta the value of record
        theta = float(sys.argv[3].split("=", 1)[1])
    else:
        header = next(l for l in open(sys.argv[3]) if l.startswith("[run] "))
        theta = float(header.split("theta=")[1].split()[0])
    try:
        table = derive(traj, run_file, alpha, theta)
    except OutsidePreRunDomain as e:
        print(f"no table: {e}")
        sys.exit(3)
    dump(table, sys.argv[4])
    if effective(stated(run_file)).condition is not Condition.INTENTION_AWARE:     # no recognition: no figure columns
        loaded = [m for m in FORBIDDEN if m in sys.modules] + [m for m in sys.modules if m.startswith("mesa_sim")]
        assert not loaded, f"the independence boundary is broken: {loaded} loaded"
        print(f"{traj['scenario']}: {len(table)} ticks ({effective(stated(run_file)).condition.value}); independence: "
              f"none of {', '.join(FORBIDDEN)} or mesa_sim loaded")
        sys.exit(0)
    # the figure's columns (plot_ir.py): the IR oracle's belief, S and lifecycle per tick, beside the compared table
    rows, _, _ = ir.run(traj, alpha, theta, ir.domain_of(run_file), bool(yaml.safe_load(open(run_file))["context_knowledge"]))
    extra = {}
    for r in rows:
        e = extra.setdefault(r["tick"], dict(belief={}, belief_h={}, S={}, lifecycle=r.get("lifecycle")))
        if r.get("key"):
            e["belief"][r["key"]] = r["belief"]
            e["belief_h"][r["key"]] = r["belief_h"]          # the belief over H (T-K part 1, AM42)
            if r.get("S") not in (None, ""):
                e["S"][r["key"]] = r["S"]
    written = json.load(open(sys.argv[4]))
    json.dump([dict(row, **extra.get(row["tick"], {})) for row in written], open(sys.argv[4], "w"), indent=0)
    loaded = [m for m in FORBIDDEN if m in sys.modules] + [m for m in sys.modules if m.startswith("mesa_sim")]
    assert not loaded, f"the independence boundary is broken: {loaded} loaded"
    print(f"{traj['scenario']}: {len(table)} ticks; independence: none of {', '.join(FORBIDDEN)} or mesa_sim loaded")
