#!/usr/bin/env python3
"""
trajectory.py — the IR test-bed's trajectory (TB.3b; design_decisions.md, "The IR test-bed", "The expectations"):
the human's sequence of actions (from TB.3b to the sort the load-time replay, world/human_executor.check_script; since
the sort the executor's stack machine, below) expanded per tick with the body's walker and timing, and the world facts
the phase rule reads, per tick. The body side of the test-bed; the expectation generator
(oracle.py) reads its output and imports nothing of the body.

    trajectory.py <run file> --length                          the last acknowledgement tick
    trajectory.py <run file> <steps> <out.json>                the expansion
    trajectory.py <run file> <steps> <out.json> <run.log>      ... and its check against the run's human lines

Independent of the layout (TB.4b): the room, the shift and the script are read from the artefacts the run file names,
the observed human is the scenario's one human, and no id, coordinate or tick is written here.

The scenario is loaded as tests/kitting/test_th2_executor.py loads it: the registered scenario with the human alone (no
robot is constructed, so no recognizer runs), from the run file's domain. Since the sort (1 October 2026) the sequence of
actions comes from the executor's own selection rule, not from the load-time replay: a StackMachine
(world/human_executor) built on the human's whole script, its repeatable entries and its closing part included, is
driven tick by tick as mesa_sim/sim_agents.HumanAgent._step_stack drives it (the acknowledged action reported done at
the start of the next tick; a during cut when its tick is reached and the action has ticks left; then next(), against
the world the environment's own builder, mesa_sim/world_state_builder.build_world_state, makes from the body state
below, mirrored into the model). Reason: under T-G A3's R1 the load-time replay does not execute repeatable entries
(the standby entry), and the selection rule is implemented once (design_decisions.md, "T-G", STAGE 1 PLAN APPROVED, the
requirement on the instruments). With the robot idle (the IR test-bed) only the human changes the world, so a Wait
with nothing in hand lasts to the run's end; the run length is read at the first Wait or Idle. The body's timing of
each action, read from mesa_sim/executor.Executor.step and mesa_sim/sim_agents.HumanAgent._step_stack:
  - every action: the executor checks the action's completion at the start of the tick, against the world built
    before the human acts (section 3); if it holds, the tick is the action's ACKNOWLEDGEMENT (no microaction,
    micro=None; ACTION_COMPLETION_LATENCY = 1), and the next action starts on the next tick (the human spends no
    per-task completion tick, HUMAN_TASK_COMPLETION_LATENCY = 0); otherwise one microaction runs;
  - STEP* (a walk): the `walk_positions` from where the action starts toward the target's position; the walk
    ends when the agent is within PROXIMITY_THRESHOLD of the target (`at` holds), short of the target point;
  - GRASP: the item is held, at the holder's position; RELEASE: the item is at the nearest fixed object, at its
    position; TOUCH (a scan): one tick, nothing physical changes (Executor._execute_touch); STAND* with a duration: that many STANDs; for an action whose completion is a world fact (wait_at) the
    last records the nearest fixed object as waited_at (cleared by the next step, grasp or release); for an action
    with process completion (stand) no STAND records anything and the action is complete once its STANDs have run
    (mesa_sim/action_decomposer._expand_stand, Executor._is_action_complete; TB.4b);
  - when an action's last microaction has run, the environment applies the declared states the action changes
    (SimModel.apply_state_changes, T-G A5), the model's own method on the mirrored model;
  - with nothing to run (Wait, Idle; after the script): the human stands, action=None, micro=None.
The world facts (mesa_sim/world_state_builder.build_world_state, the human's part): at(human, o) for every
non-held object within PROXIMITY_THRESHOLD; holding(human, item); obj_at(item, location), the location a holder
while carried; waited(human, o); and the declared states that hold (T-G A5; none in kitting), as the model holds them. The robot's facts are not produced: no hypothesis of the observed human reads
them. Tick -1 is the robot's observation before the clock starts (RobotAgent.observe_initial): the start position
and the initial world.

A mid-action cut (a DuringAction; Track 2.5, scenario_s09_13), by T-H's executed semantics (design_decisions.md,
"T-H", item 6 and the T-H2 TICKS line; mesa_sim/sim_agents.HumanAgent._step_stack step 3, Executor.suspend / resume):
  - the cut is the machine's (`cut_due` at the action's executed ticks, then `cut`); the action runs that many
    microactions and is then cut where it stands, with no acknowledgement tick: the started task's first action runs
    on the next tick;
  - the resumption (the machine's ResumeAction) completes the cut action first: a walk is
    re-expanded from the human's current position toward the target's current position (`walk_positions`, as a fresh
    walk: Executor.resume leaves a movement action an empty queue), a stand or a wait_at keeps its remaining STANDs
    (the bound duration's ticks less those done, the last still recording waited_at); a GRASP or RELEASE is never cut
    (a cut needs ticks done and ticks left);
  - the task's re-expansion follows from the machine, as any action does.
Fallback (the task prompt): if the check against the run fails, the generator is to read the run's human lines
instead; it is built only if the check fails, and the report says so.
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))

import importlib
import yaml
from shared.types import ActionStep, ConditionSchema, ProcessCompletion, ScenarioConfig, task_instance_key
from world.human_executor import ResumeAction, RunAction, StackMachine
from world.record import Record
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state, PROXIMITY_THRESHOLD
from mesa_sim.action_decomposer import walk_positions, _get_step_size, _parse_duration_to_steps
from mesa_sim.executor import ACTION_COMPLETION_LATENCY
from mesa_sim.sim_agents import HUMAN_TASK_COMPLETION_LATENCY


def domain_of(run_file):
    """The run file's domain's registry: domains/<domain>/registry.py, the place every domain keeps it."""
    return importlib.import_module(f"domains.{yaml.safe_load(open(run_file))['domain']}.registry").domain_config


def load(run_file, overrides=()):
    """The run file's scenario with the human alone, on the run file's layout (the scenario's first reference layout
    when it names none); the model (not stepped), the human's config, the scenario and the layout id. `overrides`
    (mesa_sim/overrides.py), applied by the loader as in a run; none by default (dock_loading's MPB step cap, DL-P7,
    replays a script that depends on the robot on the state after the robot's chain)."""
    cfg = yaml.safe_load(open(run_file))
    domain_config = domain_of(run_file)
    base = domain_config["scenarios"][cfg["scenario"]]
    layout = cfg.get("layout") or base.reference_layouts[0]
    human = next(a for a in base.agents if a.agent_type == "human")
    scenario = ScenarioConfig(id=base.id, description=base.description, agents=[human],
                              setup=base.setup, reference_layouts=base.reference_layouts)
    m = SimModel(scenario=scenario, register_fn=domain_config["register_fn"],
                 task_model_schemas=domain_config["task_model"],
                 layout_path=domain_config["layouts"][layout],
                 setup_path=domain_config["setups"][base.setup],
                 state_declarations=domain_config["states"], overrides=overrides)
    return m, human, base, layout


def hypothesis_durations(m, ticks_of, domain_config):
    """The body's ticks of every duration a hypothesis of this room can expect: the constants bound to a duration
    key in the methods of the task model's schemas whose every enumerated parameter has an object of its type here."""
    types = {o.type for o in m.objects.values()}
    out = {}
    for schema in domain_config["task_model"]:
        params = [p.name for p in schema.parameters if p.name not in (schema.determined_parameters or {})]
        if not all(schema.parameter_types[p] in types for p in params):
            continue
        for method in schema.methods:
            for step in method.steps:
                if not isinstance(step, ActionStep) or step.action.duration_key is None:
                    continue
                for var, val in step.bindings.items():
                    if var.name == step.action.duration_key and hasattr(val, "value"):
                        out[val.value] = ticks_of(val.value)
    return dict(sorted(out.items()))


class Body:
    """The human's body state the facts are read from: position, what it carries, where it waited, the items."""

    def __init__(self, m, start, agent):
        self.m = m
        self.agent = agent
        self.pos = tuple(start)
        self.carrying = None
        self.waited_at = None
        self.fixed = {i: tuple(o.position) for i, o in m.objects.items() if not o.is_portable and o.type != "obstacle"}
        self.item_loc = {i: o.at_location for i, o in m.objects.items() if o.is_portable}
        self.item_pos = {i: tuple(o.position) for i, o in m.objects.items() if o.is_portable}
        self.home = {i: o.home_container for i, o in m.objects.items() if o.is_portable}
        self.dest = {i: o.destination for i, o in m.objects.items() if o.is_portable and o.destination is not None}
        self.held_object = {i: o for i, o in m.objects.items() if o.is_portable}

    def position_of(self, obj):
        if obj in self.item_loc:
            return self.pos if self.item_loc[obj] is None else self.item_pos[obj]
        return self.fixed[obj]

    def nearest_fixed(self):
        return min(self.fixed, key=lambda i: math.dist(self.pos, self.fixed[i]))

    def at(self, obj):
        """at(human, obj): obj not held, within PROXIMITY_THRESHOLD."""
        if obj in self.item_loc and self.item_loc[obj] is None:
            return False
        return math.dist(self.pos, self.position_of(obj)) <= PROXIMITY_THRESHOLD

    def facts(self):
        H = self.agent
        out = [["at", H, o] for o in sorted(list(self.fixed) + list(self.item_loc)) if self.at(o)]
        if self.carrying:
            out.append(["holding", H, self.carrying])
        for i in sorted(self.item_loc):
            out.append(["obj_at", i, H if self.item_loc[i] is None else self.item_loc[i]])
        if self.waited_at:
            out.append(["waited", H, self.waited_at])
        # the declared states that hold, as the environment holds them (T-G A5; kitting declares none)
        out += sorted([f.name] + [a.value for a in f.args] for f in self.m.state_facts)
        return out

    def state_holds(self, pred):
        return pred in self.m.state_facts

    def world(self):
        """The world the environment's builder makes from this body state: the body mirrored into the model (the
        human's position, what it carries, where it waited; each item's holder, location and position), then
        build_world_state. The declared states are the model's own."""
        h = self.m.humans[self.agent]
        h.pos, h.carrying, h.waited_at = self.pos, self.carrying, self.waited_at
        for i, o in self.held_object.items():
            if self.item_loc[i] is None:
                o.held_by, o.at_location = self.agent, None
            else:
                o.held_by, o.at_location, o.position = None, self.item_loc[i], self.item_pos[i]
        return build_world_state(self.m)

    def row(self, tick, action, micro, top):
        H = self.agent
        return dict(tick=tick, x=self.pos[0], y=self.pos[1], action=action, micro=micro, task=top,
                    holding=self.carrying, waited=self.waited_at,
                    item_loc={i: (H if l is None else l) for i, l in self.item_loc.items()},
                    item_pos={i: list(self.position_of(i)) for i in self.item_loc},
                    facts=self.facts())

    # the body's microactions
    def step(self, p):
        self.pos = tuple(p)
        self.waited_at = None

    def grasp(self, item):
        self.carrying = item
        self.item_loc[item] = None
        self.waited_at = None

    def release(self):
        item, target = self.carrying, self.nearest_fixed()
        self.item_loc[item] = target
        self.item_pos[item] = self.fixed[target]
        self.carrying = None
        self.waited_at = None

    def touch(self):
        self.waited_at = None


def complete(action, body, exhausted):
    """The action's completion, from the body state (the world the executor checks at the tick's start); a process
    completion holds once the action's microactions have all run."""
    if isinstance(action.schema.completion, ProcessCompletion):
        return exhausted
    pred = action.completion_predicate
    args = [a.value for a in pred.args]
    if pred.name == "at":
        return body.at(args[1])
    if pred.name == "holding":
        return body.carrying == args[1]
    if pred.name == "obj_at":
        return body.item_loc.get(args[0]) == args[1]
    if pred.name == "waited":
        return body.waited_at == args[1]
    if pred.name in body.m.state_declarations:                       # a declared state (T-G A5)
        return body.state_holds(pred)
    raise ValueError(f"no body rule for the completion {pred}")


def expand(run_file, steps=None, overrides=()):
    m, human, base, layout = load(run_file, overrides)
    domain_config = domain_of(run_file)
    H = human.agent_id
    step_size = _get_step_size(m)
    ticks_of = lambda d: _parse_duration_to_steps(d, m)
    walk = lambda a, b: walk_positions(a, b, step_size)
    # the executor's own selection rule: a stack machine on the whole script (HumanAgent.load_stack builds the same)
    machine = StackMachine(human.scheduled_tasks, m.humans[H].machine.planner, H, ticks_of, Record())
    body = Body(m, human.start_position, H)
    rows = [body.row(-1, None, None, None)]
    boundaries = []
    in_hand = None              # the action in hand
    acked = False               # its acknowledgement was the last tick
    queue = None                # the body's remaining microactions of it (None: not expanded yet)
    done = 0                    # its executed microactions, across a cut
    last_ack = -1
    tick = 0
    while steps is None or tick < steps:
        world = body.world()                                         # the world at the tick's start
        if in_hand is not None and acked:                            # 1. reported done on the next tick
            machine.action_done(world, tick)
            in_hand, acked = None, False
        if in_hand is not None and queue and machine.cut_due(done):  # 3. a during cut: ticks executed and left
            machine.cut(world, tick, done)
            in_hand = None
        if in_hand is None:                                          # 4. what to run
            nxt = machine.next(world, tick)
            if isinstance(nxt, RunAction):
                in_hand, occurrence, done, queue = nxt.action, nxt.occurrence, 0, None
            elif isinstance(nxt, ResumeAction):
                in_hand, occurrence, done, queue = nxt.cut.action, nxt.cut.occurrence, nxt.cut.done, None
                if in_hand.schema.microactions not in ("STEP*", "STAND*"):
                    raise ValueError(f"{base.id}: a resumption of {in_hand.action_name}; a GRASP or RELEASE is never cut")
            else:                                                    # Wait or Idle: the body stands
                if steps is None:                                    # the robot idle: nothing changes from here
                    return last_ack
                rows.append(body.row(tick, None, None, None)); tick += 1
                continue
            top = task_instance_key(machine.stack_tasks()[0])
            boundaries.append(dict(tick=tick, action=in_hand.action_name, occurrence=occurrence, task=top,
                                   stack=[task_instance_key(x) for x in machine.stack_tasks()]))
        a = in_hand
        spec = a.schema.microactions
        top = task_instance_key(machine.stack_tasks()[0])
        if complete(a, body, queue == []):                           # the acknowledgement tick
            rows.append(body.row(tick, a.action_name, None, top))
            acked, last_ack = True, tick
            tick += 1
            continue
        if spec == "STEP*":
            if queue is None:
                queue = walk(body.pos, body.position_of(a.bindings[a.schema.movement_target_key]))
            body.step(queue.pop(0)); micro = "step"
        elif spec == ["GRASP"]:
            body.grasp(a.bindings[a.schema.moved_object_key]); micro = "grasp"; queue = []
        elif spec == ["RELEASE"]:
            body.release(); micro = "release"; queue = []
        elif spec == ["TOUCH"]:
            body.touch(); micro = "touch"; queue = []
        elif spec == "STAND*" and a.schema.duration_key is not None:
            if queue is None:
                queue = list(range(ticks_of(a.bindings[a.schema.duration_key]) - done, 0, -1))
            if queue.pop(0) == 1 and isinstance(a.schema.completion, ConditionSchema):
                body.waited_at = body.nearest_fixed()
            micro = "stand"
        else:
            raise ValueError(f"{base.id}: no body rule for the action {a.action_name} ({spec})")
        if not queue:                                                # its last microaction has run (T-G A5)
            m.apply_state_changes(a)
        done += 1
        rows.append(body.row(tick, a.action_name, micro, top)); tick += 1
    if steps is None:
        return last_ack
    cfg = yaml.safe_load(open(ROOT / "mesa_sim" / "mesa_configs.yaml"))["simulation"]
    params = dict(speed=step_size, beta=float(cfg["beta"]), proximity=PROXIMITY_THRESHOLD,
                  action_completion_latency=ACTION_COMPLETION_LATENCY,
                  observed_task_completion_latency=HUMAN_TASK_COMPLETION_LATENCY,
                  default_action_cost=1.0,        # mesa_sim/sim_agents.RobotAgent: a stationary action is one tick
                  duration_ticks=hypothesis_durations(m, ticks_of, domain_config))
    return dict(scenario=base.id, layout=layout, steps=steps, last_ack=last_ack, params=params,
                fixed={i: list(p) for i, p in body.fixed.items()}, home=body.home, dest=body.dest,
                types={i: o.type for i, o in m.objects.items()},
                robot_start=list(next(a for a in base.agents if a.agent_type == "robot").start_position),
                actions=boundaries, rows=rows)


def check(traj, log, agent):
    """Per tick: the expanded position rounded to the log's 2 decimals, the action and the micro, against the run's
    human lines. Returns the list of mismatches (empty: equal on every tick)."""
    AGENT = re.compile(r"\s*step: (\d+): \[" + re.escape(agent) +
                       r"\] task=(\S+) action=(\S+) micro=(\S+) pos=\[\s*(\S+)\s+(\S+)\s*\]")
    logged = {}
    for l in open(log):
        mm = AGENT.match(l)
        if mm:
            logged[int(mm[1])] = (mm[3], mm[4], float(mm[5]), float(mm[6]))
    bad = []
    rows = {r["tick"]: r for r in traj["rows"] if r["tick"] >= 0}
    if sorted(logged) != sorted(rows):
        bad.append(("ticks", sorted(set(logged) ^ set(rows))[:10]))
    for t in sorted(set(logged) & set(rows)):
        r = rows[t]
        exp = (str(r["action"]), str(r["micro"]), round(r["x"], 2), round(r["y"], 2))
        act = logged[t]
        if exp[:2] != act[:2] or abs(exp[2] - act[2]) > 1e-9 or abs(exp[3] - act[3]) > 1e-9:
            bad.append((t, exp, act))
    return bad


if __name__ == "__main__":
    run_file = sys.argv[1]
    if sys.argv[2] == "--length":
        print(expand(run_file))
        sys.exit(0)
    steps, out = int(sys.argv[2]), Path(sys.argv[3])
    traj = expand(run_file, steps)
    sid = traj["scenario"]
    json.dump(traj, open(out, "w"))
    print(f"{sid}: last acknowledgement tick {traj['last_ack']}, {steps} ticks")
    if len(sys.argv) > 4:
        human = next(a for a in domain_of(run_file)["scenarios"][sid].agents if a.agent_type == "human")
        bad = check(traj, sys.argv[4], human.agent_id)
        print(f"{sid}: trajectory against the run's human lines: "
              + ("equal on every tick" if not bad else f"{len(bad)} mismatches, first {bad[:3]}"))
        sys.exit(1 if bad else 0)
