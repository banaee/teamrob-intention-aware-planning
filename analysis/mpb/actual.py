#!/usr/bin/env python3
"""
actual.py — the meta-planner test-bed's actual side (MPB-3): the run re-executed in-process (the primary source) and the
run log (the check).

    actual.py <run file> <steps> <run.log> <last_ack> <out_dir> [--strategy S] [--assignment_prior true|false]

In-process: the same SimModel from the run file and options. Pass-through recorders on the robot's MetaPlanner INSTANCE
capture the public outputs of evaluate_triggers (the TriggerDecision, and the world the robot built that tick, whose
perception facts the fallback reads), update_human_projection (the ProjectedPlan it returns) and update (the
UpdateResult); each calls the original and returns its result unchanged. After every tick: the robot's BeliefState
(leader, boundary flag, hypothesis adequacy, observation warrant), the gate's outcome from its one home (_clears_gate,
as the IR test-bed's actual.py reads it), the decision record (_projected_hypothesis), and both agents' positions. The
model's log lines are asserted identical to the logged run's (the lines run_mesa.py itself adds removed: the per-agent
step lines, [sep], [run_mesa]): the recorders changed nothing, and the in-process run is the logged run.

Log: per fired [meta-trig], its tick, trigger and cause; the next [meta-proj] (the refusal reason, or built with its
warrant sources); the [IR] leader of the tick; [meta-cand] (single_task) and [meta-b3] (winner, hold, T_h).

Outputs in <out_dir>: actual_ticks.json, actual_decisions.json (mpblib.Decision, in-process), actual_log_decisions.json
(the log's), observed.json (the run's no_current_task ticks, its terminal tick, the comparison horizon; MPB-5),
selection.json (per decision: the winner, its hold, the horizon; [meta-cand] per candidate), robot.json (per tick the
robot's position, microaction and held item; the human's position).
"""
import json
import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim"), str(Path(__file__).resolve().parent)]

import yaml
from mpblib import Action, Admitted, Cause, Decision, Fallback, Gate, Mode, Trigger, dump

MARGIN = 30          # MPB-5: the IR test-bed's idle margin
RUN_MESA_LINES = ("  step:", "[sep]", "[run_mesa]")


class Collect(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


def in_process(run_file, steps, strategy, prior):
    from domains.kitting.registry import domain_config, register_kitting_domain
    from mesa_sim.sim_model import SimModel
    cfg = yaml.safe_load(open(run_file))
    scenario = domain_config["scenarios"][cfg["scenario"]]
    layout = cfg.get("layout") or scenario.reference_layouts[0]
    collect = Collect()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(collect)
    logging.getLogger("rec").propagate = False
    m = SimModel(scenario=scenario, register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"], layout_path=domain_config["layouts"][layout],
                 setup_path=domain_config["setups"][scenario.setup], assignment_prior=prior, strategy=strategy,
                 gate_strategy=cfg["gate_strategy"], cost_strategy=cfg["cost_strategy"],
                 separation_stop=bool(cfg["separation_stop"]), test_level=float(cfg["test_level"]))
    robot = next(iter(m.robots.values()))
    human = next(iter(m.humans.values()))
    mp = robot.meta_planner
    tick_state = {}

    def record_triggers(orig):
        def wrapped(belief, world, executor_state):
            d = orig(belief=belief, world=world, executor_state=executor_state)
            tick_state["trigger"], tick_state["world"] = d, world
            return d
        return wrapped

    def record_projection(orig):
        def wrapped(belief, world):
            tick_state["gate"] = mp._clears_gate(belief)
            tick_state["warrant"] = mp._warrant(belief)
            p = orig(belief=belief, world=world)
            tick_state["projection"] = p
            return p
        return wrapped

    def record_update(orig):
        def wrapped(**kw):
            r = orig(**kw)
            tick_state["result"] = r
            return r
        return wrapped

    mp.evaluate_triggers = record_triggers(mp.evaluate_triggers)
    mp.update_human_projection = record_projection(mp.update_human_projection)
    mp.update = record_update(mp.update)

    ticks, decisions, selection, agents = [], [], [], []
    H = human.unique_id
    for t in range(steps):
        tick_state.clear()
        n0 = len(collect.lines)
        m.step()
        b = robot.belief
        world = tick_state.get("world")
        perception = None
        if world is not None and H in world.agent_displacements:
            perception = dict(displacement=list(world.agent_displacements[H]),
                              run_length=world.agent_run_lengths[H], standing_count=world.agent_standing_counts[H])
        ticks.append(dict(tick=t, leader=b.most_likely, boundary=bool(b.episode_boundary),
                          finding=None if b.finding is None else b.finding.value,
                          gate=mp._clears_gate(b).value,
                          adequacy={k: v.value for k, v in b.hypothesis_adequacy.items()},
                          observation_warrant={k: v.value for k, v in b.observation_warrant.items()},
                          record=mp._projected_hypothesis, evaluated=world is not None, perception=perception))
        agents.append(dict(tick=t, robot=[float(robot.pos[0]), float(robot.pos[1])], micro=robot.current_microaction,
                           carrying=robot.carrying, task=None if robot.current_task_instance is None
                           else _key_task(robot.current_task_instance),
                           human=[float(human.pos[0]), float(human.pos[1])]))
        d = tick_state.get("trigger")
        if d is None or not d.fired:
            continue
        gate = Gate(tick_state["gate"].value)
        proj = tick_state["projection"]
        admitted, fb, warrant = None, None, ()
        if gate is Gate.CLEARS and proj is not None:
            held = {s.value for s in tick_state["warrant"]}
            warrant = tuple(v for v in ("commitment", "observation") if v in held)     # AD4: this order when both
            plan = proj.entries[0].abstract_plan
            admitted = Admitted(b.most_likely, tuple(Action(a.action_name, tuple(sorted(a.bindings.items())))
                                                     for a in plan.actions))
        elif proj is not None:
            seg = proj.entries[0].segments[-1]
            disp = world.agent_displacements[H]
            standing = tuple(disp) == (0.0, 0.0)
            k = world.agent_standing_counts[H] if standing else world.agent_run_lengths[H]
            fb = Fallback(Mode.STANDING if standing else Mode.MOVING, k, seg.end_step - proj.entries[0].segments[0].start_step,
                          world.timestamp + seg.end_step)
        decisions.append(Decision(t, Trigger(d.reason), None if d.cause is None else Cause(d.cause.value), gate,
                                  b.most_likely, warrant, admitted, fb))
        r = tick_state.get("result")
        new = collect.lines[n0:]
        cands = [dict(task=l.split()[1], delta=int(re.search(r" delta=(\d+)", l)[1]),
                      T_r=float(re.search(r" T_r=([\d.]+)", l)[1])) for l in new if l.startswith("[meta-cand]")]
        selection.append(dict(tick=t, trigger=d.reason, terminal=r is None or r.current_task is None,
                              winner=None if r is None or r.current_task is None else _key_task(r.current_task),
                              hold=None if r is None else r.hold, horizon=None if r is None else r.horizon,
                              candidates=cands))
    root.removeHandler(collect)
    return collect.lines, ticks, decisions, selection, agents


def _key_task(task):
    """A task instance key as the logs print it (task_instance_key's form): the schema and every binding, sorted."""
    return f"{task.schema.name}(" + ",".join(f"{v.name}={c.value}" for v, c in
                                             sorted(task.bindings.items(), key=lambda kv: kv[0].name)) + ")"


TRIG = re.compile(r"^\[meta-trig\] step=(\d+) trigger=(\S+)(?: cause=(\S+))?$")
PROJ = re.compile(r"^\[meta-proj\] confidence=\S+ theta=\S+ projection=(.*)$")
IRL = re.compile(r"^\[IR\] step=(-?\d+) most_likely=(\S+) ")


def from_log(log_path):
    """Per fired trigger of the log: tick, trigger, cause, the [meta-proj] projection text, the tick's [IR] leader."""
    leader, out, cur = {}, [], None
    for l in open(log_path):
        l = l.rstrip("\n")
        m = IRL.match(l)
        if m:
            leader[int(m[1])] = None if m[2] == "none" else m[2]
            continue
        m = TRIG.match(l)
        if m and m[2] != "none":
            cur = dict(tick=int(m[1]), trigger=m[2], cause=m[3], leader=leader.get(int(m[1])), projection=None)
            out.append(cur)
            continue
        m = PROJ.match(l)
        if m and cur is not None and cur["projection"] is None:
            cur["projection"] = m[1]
    return out


if __name__ == "__main__":
    run_file, steps, log_path, last_ack, out = (sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]),
                                               Path(sys.argv[5]))
    strategy = sys.argv[sys.argv.index("--strategy") + 1] if "--strategy" in sys.argv else "single_task"
    prior = (sys.argv[sys.argv.index("--assignment_prior") + 1] == "true") if "--assignment_prior" in sys.argv \
        else bool(yaml.safe_load(open(run_file))["assignment_prior"])
    out.mkdir(parents=True, exist_ok=True)
    lines, ticks, decisions, selection, agents = in_process(run_file, steps, strategy, prior)
    logged = [l.rstrip("\n") for l in open(log_path) if not l.startswith(RUN_MESA_LINES)]
    same = lines == logged
    print(f"{run_file}: in-process model lines {'identical to' if same else 'DIFFER from'} the logged run's "
          f"({len(lines)} lines)")
    assert same, "the in-process run is not the logged run"
    nct = [d.tick for d in decisions if d.trigger is Trigger.NO_CURRENT_TASK]
    terminal = next((s["tick"] for s in selection if s["terminal"]), None)
    first_complete = None if terminal is None else max(last_ack + 1, terminal)
    horizon = steps if first_complete is None else min(steps, first_complete + MARGIN)
    json.dump(dict(no_current_task=nct, terminal=terminal, last_ack=last_ack, steps=steps, horizon=horizon,
                   strategy=strategy, prior=prior), open(out / "observed.json", "w"), indent=1)
    json.dump(ticks, open(out / "actual_ticks.json", "w"))
    dump(decisions, out / "actual_decisions.json")
    json.dump(from_log(log_path), open(out / "actual_log_decisions.json", "w"), indent=0)
    json.dump(selection, open(out / "selection.json", "w"), indent=0)
    json.dump(agents, open(out / "robot.json", "w"))
    print(f"  decisions {len(decisions)}, no_current_task {nct}, terminal {terminal}, horizon {horizon}")
