#!/usr/bin/env python3
"""
oracle.py — the IRB's expectation generator (IRB.3b; design_decisions.md, "The intention-recognition test-bed (IRB)", "Independence
boundary"): the recognizer's outputs per tick, derived from the recognizer records at HEAD and from nothing of the
recognizer's code.

    oracle.py <trajectory.json> <run file> <expected.csv> <phases.json> <run.log | theta=<value>> [context=on|off]

T-K part 1's gate stage (rule 28): the leader and its confidence from the belief over H. T-K part 1's build, stage 6
(rules 29 to 33): with context knowledge on (the run file's `context_knowledge`, or `context=on|off` given), the
prior from the domain's declared context knowledge (its registry's "context_knowledge": the declared values are read
as the task model is; the levels, the groups and the division are computed here from the method document,
docs/context_knowledge_method.md, sections 3, 4 and 6, not by shared/recognizer.py), its own memory of observed
completions from the rows (AM47), and the columns `prior` per key and `levels` per tick.

Independence. It imports nothing from shared/recognizer.py or shared/likelihood_functions.py, and asserts at the end
that neither module was loaded in its process. It uses the planner's decomposition (`AdaptivePlanner.decompose`, on
the robot's task model) and the domain's method guards for each hypothesis's expected action sequence: the domain's
structure, not the recognizer's. Its input is the per-tick trajectory and world facts (trajectory.py), the body's
parameters it carries, and α from the run file.

Each rule is marked with its source: HB = docs/recognizer_handback.md, DD = design_decisions.md "T-D R and E" (with
its "1.5 rulings"), DL = design_decisions.md "T-D L: the belief lifecycle" as amended on the L-records report (L-build,
27 September 2026), and the four readings confirmed at the IRB.3b plan step (R1 to R4, analysis/irb/README.md).
L-build changed three rules by derivation from DL (README, "L-build"): the boundary (DL L1, in the entry's own words
for the domain's two terminal actions, not through the schemas' preconditions as the recognizer reads it), liveness
and re-entry (DL L4, arithmetic C, computed after the normalisation over the incumbents rather than before it), and a
new per-tick column, the re-entries.
G-build added two columns by derivation from DG = design_decisions.md "T-D G: admission" (AD1, AD4) and the ruling at
the G-build plan step on an unresolved target (README, "G-build"): the observation warrant per hypothesis, and the
gate's expected outcome per tick (θ from the run log's [run] header, the one value read from the log; commitment from
the scenario's assigned tasks, by the support's key reading, rule 1).
The sort and dock_loading (1 October 2026; analysis/instruments/irb/README.md, rules 24 to 27): the domain from
the run file; the agent's area in the world of a tick (the layout's declared areas and the one definition,
shared.types.area_fact; T-G A9, R2); liveness by applicability (T-G A4; HB §1.1, its A4 amendment); and the boundary
also read through each terminal action's preconditions and completion condition (DL L1 as amended, its as-built
reading), which covers a terminal action other than place and wait_at (dock_loading's scan_it).
The gate rulings' build, stage 4 (4 October 2026; rules 34 to 36 in kitting's README, "The gate rulings' build"):
the gate without commitment warrant (AM67: observation warrant for every hypothesis), the column `rank` per hypothesis
from the generator's own evidence (AM68, AM73, AM75, AM76: outranked iff another live hypothesis's evidence is strictly
greater), `undetermined` where the leader's or a key's evidence lies within the comparison's agreement level of
another's (D3: the rule is exact, the tolerance is the instrument's; skipped and counted by compare.py), and the gate's
last refusal `none(leader_outranked)` (D1), `undetermined` when it turns on an undetermined rank.
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import importlib
import itertools
import yaml
from shared.types import (ActionStep, AgentState, Area, Const, PersonalTask, Predicate, TaskInstance, Var, WorkTask,
                          WorldState, area_fact, task_instance_key)
from shared.knowledge import ObjectState, RecencyFact, TaskModel, TimelineFact
from shared.planner import AdaptivePlanner, DecompositionError


def domain_of(run_file):
    """The run file's domain's registry: domains/<domain>/registry.py, the place every domain keeps it."""
    return importlib.import_module(f"domains.{yaml.safe_load(open(run_file))['domain']}.registry").domain_config


def areas_of(domain_config, layout):
    """The layout's declared areas, in declaration order, as the environment reads them (SimModel; T-G A9)."""
    env_layout = json.load(open(ROOT / domain_config["layouts"][layout]))
    return tuple(Area(id=a["id"], x_min=a["bounds"]["x_min"], x_max=a["bounds"]["x_max"],
                      y_min=a["bounds"]["y_min"], y_max=a["bounds"]["y_max"]) for a in env_layout.get("areas", []))

# HB §2: the recognizer's constants; HB §1.7 / §2: BELIEF_FLOOR (output only).
HIT, FALSE_ALARM, FLOOR = 1.0, 1e-3, 1e-3


# ---- the hypothesis space and the support (HB §1.1) -------------------------------------------------------------
def key_of(schema, binding):
    """A hypothesis key as the recognizer prints it: the schema and its ENUMERATED bindings (glossary §5)."""
    return f"{schema.name}(" + ",".join(f"{p}={v}" for p, v in binding) + ")"


def hypothesis_space(task_model, types):
    """One hypothesis per task schema of the robot's task model and typed binding of its enumerated parameters
    (determined parameters are not enumerated); keys sorted (HB §1.1)."""
    space = {}
    for schema in task_model.task_schemas():
        params = [p.name for p in schema.parameters if p.name not in (schema.determined_parameters or {})]
        combos = [[]]
        for p in params:
            objs = sorted(i for i, t in types.items() if t == schema.parameter_types[p])
            combos = [c + [(p, o)] for c in combos for o in objs]
        for c in combos:
            if params and not c:
                continue
            task = TaskInstance(schema=schema, bindings={Var(p): Const(v) for p, v in c})
            space[key_of(schema, c)] = task
    return dict(sorted(space.items()))


def known_keys(assigned):
    """The assigned tasks' hypothesis keys: each task's schema and enumerated bindings (HB §1.1)."""
    known = set()
    for t in assigned:
        params = [p for p in t.schema.parameters if p.name not in (t.schema.determined_parameters or {})]
        known.add(key_of(t.schema, [(p.name, t.bindings[p].value) for p in params]))
    return known


def support(space, assigned):
    """Prior on: the assigned tasks and every foreseeable task (a PersonalTask's hypothesis) (HB §1.1)."""
    known = known_keys(assigned)
    return {k for k, t in space.items() if k in known or isinstance(t.schema, PersonalTask)}


# ---- the world of a tick, from the trajectory --------------------------------------------------------------------
def world_of(row, traj, agent, areas):
    preds = {Predicate(f[0], tuple(Const(a) for a in f[1:])) for f in row["facts"]}
    fact = area_fact(agent, (row["x"], row["y"]), areas)             # the agent's area (T-G A9, R2)
    if fact is not None:
        preds.add(fact)
    positions = {i: tuple(p) for i, p in traj["fixed"].items()}
    positions.update({i: tuple(p) for i, p in row["item_pos"].items()})
    return WorldState(timestamp=float(row["tick"]),
                      agent_states={agent: AgentState(agent_id=agent, holding=row["holding"])},
                      agent_positions={agent: (row["x"], row["y"])},
                      object_locations=dict(row["item_loc"]), predicates=preds,
                      object_home_container=dict(traj["home"]), object_destination=dict(traj["dest"]),
                      object_positions=positions, areas=areas)


def target_position(obj, world):
    """The target's CURRENT position; a carried object resolves through its holder (HB §1.4, target resolution)."""
    holder = world.object_locations.get(obj)
    if holder is not None and holder in world.agent_positions:
        return world.agent_positions[holder]
    return world.object_positions.get(obj)


def sig(a):
    """Two actions are the same when their name and grounded bindings are (HB §1.3)."""
    return None if a is None else (a.action_name, tuple(sorted(a.bindings.items())))


def label(a):
    return "-" if a is None else a.action_name + "(" + ",".join(
        f"{k}={v}" for k, v in sorted(a.bindings.items()) if k != "?agent") + ")"


class ContextPrior:
    """
    The prior from the declared context knowledge (T-K part 1; docs/context_knowledge_method.md, sections 3, 4, 6;
    design_decisions.md "T-K", R3, R4, AM35 to AM38, AM44, AM47), derived here from the domain's declarations and
    the rows' facts; nothing of shared/recognizer.py.
    - Rule 29, the facts (section 3): a timeline fact holds iff its name is among the row's facts with no argument; an
      object state iff a fact of its name with one argument is among them (any object of its type, AM44); a recency
      fact of task f iff this oracle's memory holds an observed completion of f at t_obs with 0 <= t - t_obs < d_f.
    - Rule 30, the memory (AM47): per hypothesis of a task that declares a recency duration, its terminal fact (the
      decomposition's last completion predicate, as the pin reads it) newly holding after a tick on which it did
      not (read, applicable) is an observed completion of the task at that tick; d_f from the trajectory's
      recency_ticks (the body's conversion).
    - Rule 31, the level (section 4): suppressed if the suppressing condition (every fact of its conjunction) is
      satisfied; else raised if the raising condition is; else ordinary. The suppressed and the ordinary strength are
      the domain's, the raised strength the task's.
    - Rule 32, the weights (section 6): the live WorkTask hypotheses share 1 equally (nothing when none is live);
      each foreseeable task's live hypotheses share its strength equally; pi = w / sum(w).
    - Rule 33, the belief (section 7): B = normalise(E x w) over H; the reported distribution P applies the floor and
      the pins to B (rule 15); the leader and its confidence read B (rule 28).
    """

    def __init__(self, knowledge, space, recency_ticks):
        self.k = knowledge                          # the declared values: suppressed, ordinary, entries()
        self.entries = knowledge.entries()          # per task its ForeseeableKnowledge; the lookup is this class's own
        self.space = space                          # key -> TaskInstance
        self.ticks = recency_ticks                  # task name -> d_f in ticks
        self.held = {}                              # key -> whether its terminal fact held last tick (None: not read)
        self.completed = {}                         # task name -> the tick of its last observed completion

    def observe(self, t, key, actions):
        """Rule 30: `actions` the decomposition this tick (None: not applicable)."""
        task = self.space[key].schema
        if task.name not in self.ticks:
            return
        if actions is None:
            self.held[key] = None
            return
        pred = actions[-1].completion_predicate
        holds = pred is not None and pred in self.world_predicates
        if holds and self.held.get(key) is False:
            self.completed[task.name] = t
        self.held[key] = holds

    def recent(self, t):
        return {name for name, t0 in self.completed.items() if 0 <= t - t0 < self.ticks[name]}

    def fact_holds(self, f, facts, recent):
        if isinstance(f, TimelineFact):
            return (f.state.name,) in facts
        if isinstance(f, ObjectState):
            return any(x[0] == f.state.name and len(x) == 2 for x in facts)
        if isinstance(f, RecencyFact):
            return f.task.name in recent
        raise TypeError(f)

    def entry(self, task):
        return next(e for e in self.entries if e.task is task)

    def level(self, task, facts, recent):
        e = self.entry(task)
        if e.suppressing is not None and all(self.fact_holds(f, facts, recent) for f in e.suppressing.facts):
            return "suppressed"
        if e.raising is not None and all(self.fact_holds(f, facts, recent) for f in e.raising.facts):
            return "raised"
        return "ordinary"

    def strength(self, task, lev):
        return {"suppressed": self.k.suppressed, "ordinary": self.k.ordinary}.get(lev, self.entry(task).raised).value

    def weights(self, t, live, facts):
        """Rules 31 and 32: the weights over the live keys and the levels per foreseeable task with a live key."""
        recent = self.recent(t)
        work = [k for k in live if isinstance(self.space[k].schema, WorkTask)]
        groups = {}
        for k in live:
            if k not in work:
                groups.setdefault(self.space[k].schema.name, []).append(k)
        levels = {name: self.level(self.space[keys[0]].schema, facts, recent) for name, keys in groups.items()}
        w = {k: 1.0 / len(work) for k in work}
        for name, keys in groups.items():
            s = self.strength(self.space[keys[0]].schema, levels[name])
            w.update({k: s / len(keys) for k in keys})
        return w, levels, sorted(recent)


class Oracle:
    def __init__(self, traj, alpha, theta, domain_config, context=False):
        p = traj["params"]
        self.v, self.beta, self.alpha, self.theta = p["speed"], p["beta"], alpha, theta
        self.lat_action, self.lat_task = p["action_completion_latency"], p["observed_task_completion_latency"]
        self.default_cost, self.duration_ticks = p["default_action_cost"], p["duration_ticks"]
        self.traj = traj
        task_model = TaskModel(domain_config["register_fn"](), domain_config["task_model"])
        self.planner = AdaptivePlanner(knowledge=task_model)
        self.areas = areas_of(domain_config, traj["layout"])
        # DL L1: the terminal actions, the last action of some method of a task schema of the robot's task model
        terminal = {m.steps[-1].action.name: m.steps[-1].action for s in task_model.task_schemas() for m in s.methods
                    if m.steps and isinstance(m.steps[-1], ActionStep)}
        self.terminal = [terminal[name] for name in sorted(terminal)]
        self.objects = sorted(traj["types"])
        self.space = hypothesis_space(task_model, traj["types"])
        human = next(a for a in domain_config["scenarios"][traj["scenario"]].agents if a.agent_type == "human")
        self.agent = human.agent_id                    # the observed human: the scenario's one human
        self.admissible = support(self.space, human.assigned_tasks)
        live = sorted(self.admissible)
        # HB §1.2: the uniform prior over the live set at construction
        self.base = {k: 1.0 / len(live) for k in live}
        self.expected, self.origin, self.entry = {}, {}, {}
        self.observed, self.completed = set(), set()
        self.inapplicable = set()                     # T-G A4: the keys not live for want of an applicable method
        # DG AD1: the keys whose current phase was entered by the completion of the previous expected action in this
        # episode (the completion E8 reads): reset at a boundary and at every phase change, a first observation or a pin
        self.entered = set()
        self.last_pos, self.odo, self.still = None, 0.0, 0
        self.prev_facts = None                         # the previous tick's world facts, for the boundary (DL L1)
        # T-K part 1 (rules 29 to 33): the prior from the declared context knowledge, with context knowledge on
        self.context = ContextPrior(domain_config["context_knowledge"], self.space,
                                    traj["params"]["recency_ticks"]) if context else None

    # ---- the phase term (HB §1.4, §1.8, §1.10; DD E2, E9, E10) ---------------------------------------------------
    def s_exp(self, k, a):
        """E9: the latency priced to the phase at its entry, plus the action's own stationary duration: 0 for a walk,
        the bound duration in ticks for an action with a duration binding (wait_at), else the body's default action
        cost (pick_up, place) (HB §1.10, the ruling "the source of s_exp")."""
        if a.schema.movement_target_key is not None:
            own = 0.0
        elif a.schema.duration_key is not None and a.bindings.get(a.schema.duration_key) is not None:
            own = float(self.duration_ticks[a.bindings[a.schema.duration_key]])
        else:
            own = self.default_cost
        return self.entry[k] + own

    def phase(self, k, a, pos, world):
        """The phase's statistic from k's origin: w, e, s, s_exp, D and L (HB §1.4 formula, §1.8 λ)."""
        if a is None:                                  # no derived phase: L = 1 (HB §1.4, NO DERIVED PHASE)
            return dict(w=None, e=None, s=None, s_exp=None, D=None, vD=None, L=1.0)
        o, o_odo, o_still = self.origin[k]
        w = self.odo - o_odo
        s = self.still - o_still
        e = 0.0
        tgt = a.bindings.get(a.schema.movement_target_key) if a.schema.movement_target_key else None
        g = target_position(tgt, world) if tgt is not None else None
        if a.schema.progress_evaluator is not None and g is not None and w > 0:
            e = w + math.dist(pos, g) - math.dist(o, g)   # straight-line path cost C (HB §1.4)
        sx = self.s_exp(k, a)
        vD = e + self.v * (s - sx)
        L = 2.0 / (1.0 + math.exp(self.beta * vD)) if vD > 0 else 1.0   # clipped at 1 (E10, HB §1.4)
        return dict(w=w, e=e, s=s, s_exp=sx, D=vD / self.v, vD=vD, L=L)

    def tail(self, vD):
        """E5: S(x) = ln(1 + e^(−βx)) / ln 2, and 1 for x ≤ 0."""
        return 1.0 if vD <= 0 else math.log(1.0 + math.exp(-self.beta * vD)) / math.log(2.0)

    # ---- one update (HB §1.8) ---------------------------------------------------------------------------------------
    def update(self, row):
        world = world_of(row, self.traj, self.agent, self.areas)
        holds = lambda p: p is not None and p in world.predicates
        pos = (row["x"], row["y"])
        step = 0.0 if self.last_pos is None else math.dist(pos, self.last_pos)   # 0 on the first observation
        self.odo += step
        self.still += (step == 0)
        self.last_pos = pos
        mu = None if row["micro"] is None else row["micro"].upper()
        boundary = self.terminal_completed(row["facts"])                     # DL L1
        pins, reentries, advanced, U, folds = [], [], set(), {}, {}
        if self.context is not None:
            self.context.world_predicates = world.predicates
        for k in sorted(self.admissible):                  # every admissible key; live: its terminal fact not holding
            try:
                A = self.planner.decompose(self.space[k], self.agent, world)
            except DecompositionError:
                A = None
            if self.context is not None:
                self.context.observe(row["tick"], k, A)     # rule 30: before the recognizer's reading, as the memory does
            if A is None and k not in self.completed:     # T-G A4: no applicable method: not live (HB §1.1)
                if k not in self.inapplicable:
                    self.inapplicable.add(k)
                    for d in (self.base, self.expected, self.origin, self.entry):
                        d.pop(k, None)
                    self.observed.discard(k)
                    self.entered.discard(k)
                continue
            if A is not None and holds(A[-1].completion_predicate):             # the terminal pin (HB §1.6)
                self.inapplicable.discard(k)               # T-G A4: applicable again, its fact holding: retired
                if k not in self.completed:                # retired while the fact holds (DL L4)
                    self.completed.add(k); pins.append(k)
                    for d in (self.base, self.expected, self.origin, self.entry):
                        d.pop(k, None)
                    self.observed.discard(k)
                    self.entered.discard(k)
                continue
            if k in self.completed:
                if A is None:                              # its fact cannot be read: nothing says it stopped
                    continue
                self.completed.discard(k); reentries.append(k)                  # live again (DL L4)
            elif k in self.inapplicable:                   # T-G A4: applicable again: re-enters through L4's path
                self.inapplicable.discard(k); reentries.append(k)
            a = next((x for x in A if not holds(x.completion_predicate)), None) if A is not None else None
            if k not in self.observed:                   # enters its action from no completion: an empty phase
                self.observed.add(k)
                self.expected[k], self.origin[k], self.entry[k] = a, (pos, self.odo, self.still), 0.0
                self.entered.discard(k)                                          # DG AD1: no completion
                if k not in reentries:
                    U[k] = self.base[k]
                continue
            a_prev = self.expected[k]
            # the completion signal (HB §1.4; reading R1: only a declared microaction list, GRASP / RELEASE)
            if a_prev is not None and isinstance(a_prev.schema.microactions, list) \
                    and mu in [x.upper() for x in a_prev.schema.microactions]:
                self.base[k] *= HIT if holds(a_prev.completion_predicate) else FALSE_ALARM
            if sig(a_prev) != sig(a):                      # a phase advance or regress: the fold (HB §1.5)
                closing = self.phase(k, a_prev, pos, world)
                folds[k] = (label(a_prev), closing)
                self.base[k] *= closing["L"]
                self.expected[k], self.origin[k] = a, (pos, self.odo, self.still)
                done = a_prev is not None and holds(a_prev.completion_predicate)
                self.entry[k] = self.lat_action if done else 0.0                # E9
                if done:
                    advanced.add(k)                                              # E8
                    self.entered.add(k)                                          # DG AD1: the entry source
                else:
                    self.entered.discard(k)                                      # DG AD1: reset at a phase change
            U[k] = self.base[k] * self.phase(k, a, pos, world)["L"]
        Z = sum(U.values())                                # one normalisation, over H (HB §1.5)
        if Z > 0:
            self.base = {k: v / Z for k, v in self.base.items() if k not in reentries}
            E = {k: v / Z for k, v in U.items()}
        else:
            self.base = {k: v for k, v in self.base.items() if k not in reentries}
            E = {}
        if reentries:
            # DL L4, re-entry C: each returning hypothesis takes exactly 1/|H| (H with it); the incumbents share the rest
            # in their existing proportions (this tick's, after their update); the base of a first observation is its
            # evidence (open value 1)
            n = len(E) + len(reentries)
            scale = (n - len(reentries)) / n
            E = {k: v * scale for k, v in E.items()}
            self.base = {k: v * scale for k, v in self.base.items()}
            for k in reentries:
                E[k] = self.base[k] = 1.0 / n
        if boundary and self.base:                         # the episode boundary (HB §1.6, §1.8)
            n = len(self.base)
            self.base = {k: 1.0 / n for k in self.base}
            E = dict(self.base)
            for k in self.base:
                self.origin[k] = (pos, self.odo, self.still)
                self.entry[k] = self.lat_action + self.lat_task                  # E9
            advanced = set()                                                     # E8: no observation on it
            self.entered = set()                                                 # DG AD1: reset with the origins
        return world, E, pins, reentries, boundary, advanced, folds

    def terminal_completed(self, facts):
        """DL L1 as amended, in the entry's words: the observed agent completes a terminal action on this tick iff the
        release leaves the object it held on the previous tick placed at a container (`place`: holding(h, x) held, and
        now x is no longer held and obj_at(x, c) holds for a c that is not an agent), or waited(h, ·) starts holding
        (`wait_at`). Read from the world's facts; no microaction. None on the first observation."""
        now = {tuple(f) for f in facts}
        prev, self.prev_facts = self.prev_facts, now
        if prev is None:
            return False
        h = self.agent
        agents = {self.agent} | {f[1] for f in now | prev if f[0] == "holding"}
        for f in prev:
            if f[0] == "holding" and f[1] == h and ("holding", h, f[2]) not in now:
                if any(g[0] == "obj_at" and g[1] == f[2] and g[2] not in agents for g in now):
                    return True
        if any(f[0] == "waited" and f[1] == h and f not in prev for f in now):
            return True
        return any(self.completes(T, h, prev, now) for T in self.terminal)

    def completes(self, T, h, prev, now):
        """DL L1 as amended, its as-built reading, for any terminal action T: T's preconditions held for the observed
        agent on the previous tick and, under that binding, a grounding of its completion condition holds now that did
        not then (scan_it: at(h, x) then, is_scanned(x) newly now). The variables range over the objects; ?agent is h."""
        conds = list(T.preconditions) + [T.completion]
        names = sorted({a.name for c in conds for a in c.args if isinstance(a, Var) and a.name != "?agent"})
        for values in itertools.product(self.objects, repeat=len(names)):
            b = dict(zip(names, values), **{"?agent": h})
            ground = lambda c: (c.name,) + tuple(b[a.name] if isinstance(a, Var) else a.value for a in c.args)
            if all(ground(c) in prev for c in T.preconditions):
                g = ground(T.completion)
                if g in now and g not in prev:
                    return True
        return False

    def warrant(self, k, pos, world):
        """DG AD1: observation warrant. The entry source, for any phase: the phase was entered by a completion in this
        episode. The movement source, for a phase with a movement target: the gain toward the target's current position
        since the phase origin is positive, dist(o, g) - dist(p, g) > 0 (straight-line C, rule 9's path cost). None for a
        stationary phase (no movement target), for a move_to whose target has no position (no gain computable; the
        plan-step ruling), and with no derived phase."""
        a = self.expected.get(k)
        if a is None:
            return "none"
        if k in self.entered:
            return "observation"
        if a.schema.movement_target_key is None:
            return "none"
        g = target_position(a.bindings.get(a.schema.movement_target_key), world)
        if g is None:
            return "none"
        return "observation" if math.dist(self.origin[k][0], g) - math.dist(pos, g) > 0 else "none"

    def gate(self, ml, conf, per):
        """DG AD1, AD4 (and G1), AM67, AM68 (rules 23, 35): the gate's outcome on the leader: below θ; else its
        hypothesis adequacy, inadequate then no observation; else its observation warrant (commitment warrant admits
        nothing since AM67); else its rank, asked last (D1): outranked refuses, undetermined (D3) leaves the outcome
        undetermined; else it clears. Exhausted: no leader, confidence 0, below θ."""
        if ml is None or conf < self.theta:
            return "none(below_theta)"
        adequacy, warrant, rank = per[ml][3], per[ml][4], per[ml][5]
        if adequacy == "inadequate":
            return "none(leader_inadequate)"
        if adequacy != "adequate":
            return "none(leader_no_observation)"
        if warrant != "observation":
            return "none(leader_unwarranted)"
        if rank == "outranked":
            return "none(leader_outranked)"
        if rank == UNDETERMINED:
            return UNDETERMINED
        return "clears"

    def output(self, E, t, facts):
        """HB §1.7 (reading R2): the reported distribution P: normalise over H, the floor, the pinned keys at the
        floor, the live keys scaled to 1 − FLOOR·|pinned|. Since T-K part 1 (rules 32, 33): E is multiplied by the
        prior's weights first with context knowledge on (every weight 1 with it off: ω's place, HB §2, now the
        equal prior). The leader and its confidence (rule 28, AM42): the argmax of the belief over H (B, before the
        floor and the pins) and its value there, not P's. Returns P, B, the leader, its confidence, pi over H and
        the levels (empty with context knowledge off)."""
        pinned = [k for k in self.space if k not in E]
        P = {k: FLOOR for k in pinned}
        pi, levels, recent = {}, {}, []
        if E:
            if self.context is not None:
                w, levels, recent = self.context.weights(t, sorted(E), facts)
                z = sum(w.values())
                pi = {k: w[k] / z for k in E}
                U = {k: v * w[k] for k, v in E.items()}
            else:
                U = dict(E)
            tot = sum(U.values())
            B = {k: v / tot for k, v in U.items()}       # the belief over H (rules 28, 33)
            r = {k: max(v, FLOOR) for k, v in B.items()}
            sr = sum(r.values())
            P.update({k: v / sr * (1.0 - FLOOR * len(pinned)) for k, v in r.items()})
            ml = max(sorted(B), key=lambda k: B[k])      # ties to the first live key in sorted order
            return P, B, ml, B[ml], pi, levels, recent
        return P, {}, None, 0.0, pi, levels, recent

    def adequacy(self, k, pos, world, boundary, advanced):
        """Membership as amended twice with the boundary-tick rule, reading R3 (DD E6, E8; HB §1.10); S (E5)."""
        a = self.expected.get(k)
        ph = self.phase(k, a, pos, world)
        if a is None or boundary:
            return ph, False, None
        stationary = a.schema.movement_target_key is None
        member = (ph["w"] > 0 or ph["s"] > ph["s_exp"]
                  or (ph["s"] <= ph["s_exp"] and (stationary or ph["s_exp"] > 0)) or k in advanced)
        if not member:
            return ph, False, None
        return ph, True, 1.0 if k in advanced else self.tail(ph["vD"])


# D3 (rule 34): the generator's evidence agrees with the recognizer's at this level (compare.py's numeric tolerance),
# not bit for bit; where two keys' evidence lie within it, the exact rule's answer (AM75) is not determined here
AGREEMENT = dict(rel_tol=1e-9, abs_tol=1e-12)
UNDETERMINED = "undetermined"


def rank(E, k):
    """AM68, AM73, AM75, AM76 (rule 34): outranked iff another live key's evidence is strictly greater; not_outranked
    iff none is (a tie included); undetermined (D3) where no other key is greater beyond the agreement level and some
    other key lies within it, either side, without being equal. D3 AMENDED (Hadi, 5 October 2026): an other key whose
    evidence here is exactly equal is a tie, not outranked (the re-entry rule's 1/|H| makes such ties by
    construction), so the comparison checks that a tie passes."""
    others = [v for j, v in E.items() if j != k]
    if any(v > E[k] and not math.isclose(v, E[k], **AGREEMENT) for v in others):
        return "outranked"
    if any(v != E[k] and math.isclose(v, E[k], **AGREEMENT) for v in others):
        return UNDETERMINED
    return "not_outranked"


COLUMNS = ["tick", "human_x", "human_y", "micro", "holding", "waited", "obj_at", "at", "most_likely", "confidence",
           "finding", "lifecycle", "pins", "reentries", "boundary", "gate", "levels", "recent", "key", "expected_action",
           "origin_x", "origin_y", "e", "s", "s_exp", "D", "L", "evidence", "prior", "belief", "belief_h", "S", "member",
           "adequacy", "warrant", "rank"]


def run(traj, alpha, theta, domain_config, context=False):
    orc = Oracle(traj, alpha, theta, domain_config, context)
    rows, phases = [], {k: [] for k in orc.space}
    for r in traj["rows"]:
        world, E, pins, reentries, boundary, advanced, folds = orc.update(r)
        P, B, ml, conf, pi, levels, recent = orc.output(E, r["tick"], {tuple(f) for f in r["facts"]})
        pos = (r["x"], r["y"])
        live = sorted(orc.base)
        per = {}
        for k in live:
            ph, member, S = orc.adequacy(k, pos, world, boundary, advanced)
            adequacy = "no_observation" if not member else ("adequate" if S >= alpha else "inadequate")
            per[k] = (ph, member, S, adequacy, orc.warrant(k, pos, world), rank(E, k))
            a = orc.expected.get(k)
            if not phases[k] or phases[k][-1][0] != label(a):
                phases[k].append([label(a), r["tick"], r["tick"]])
            else:
                phases[k][-1][2] = r["tick"]
        if not live:
            lifecycle, finding = "exhausted", None
        else:
            lifecycle = "live"
            members = [v for v in per.values() if v[1]]
            finding = ("unresolved" if not members else
                       "unexplained" if all(v[2] < alpha for v in members) else "adequate")
        # R6 at level (1): the evidence sums to 1 over exactly H
        assert not E or (abs(sum(E.values()) - 1.0) < 1e-12 and set(E) == set(live)), r["tick"]
        common = dict(tick=r["tick"], human_x=r["x"], human_y=r["y"], micro=r["micro"], holding=r["holding"],
                      waited=r["waited"], obj_at=";".join(f"{i}@{l}" for i, l in sorted(r["item_loc"].items())),
                      at=";".join(f[2] for f in r["facts"] if f[0] == "at"), most_likely=ml, confidence=conf,
                      finding=finding, lifecycle=lifecycle, pins=";".join(pins), reentries=";".join(reentries),
                      boundary=int(boundary), gate=orc.gate(ml, conf, per),
                      levels=" ".join(f"{n}={v}" for n, v in sorted(levels.items())), recent=" ".join(recent))
        if not live:
            rows.append(dict(common))
        for k in live:
            ph, member, S, adequacy, warrant, rk = per[k]
            o = orc.origin[k][0]
            rows.append(dict(common, key=k, expected_action=label(orc.expected.get(k)), origin_x=o[0], origin_y=o[1],
                             e=ph["e"], s=ph["s"], s_exp=ph["s_exp"], D=ph["D"], L=ph["L"], evidence=E[k],
                             prior=pi.get(k), belief=P[k], belief_h=B[k], S=S, member=int(member), adequacy=adequacy,
                             warrant=warrant, rank=rk))
    return rows, phases, sorted(orc.admissible)


if __name__ == "__main__":
    traj = json.load(open(sys.argv[1]))
    alpha = float(yaml.safe_load(open(sys.argv[2]))["test_level"])
    # θ, the meta-planner's, from the run's [run] header (shared.meta_planner would load the recognizer); before the
    # run (the expectations committed before any run, since the sort) the value of record, given as theta=<value>,
    # and the run's own oracle call must then reproduce the committed expected.csv
    if sys.argv[5].startswith("theta="):
        theta = float(sys.argv[5].split("=", 1)[1])
    else:
        header = next(l for l in open(sys.argv[5]) if l.startswith("[run] "))
        theta = float(header.split("theta=")[1].split()[0])
    # context knowledge: the run file's option, or context=on|off given (run.sh's --context, T-K part 1, stage 6)
    context = bool(yaml.safe_load(open(sys.argv[2]))["context_knowledge"])
    if len(sys.argv) > 6 and sys.argv[6].startswith("context="):
        context = sys.argv[6].split("=", 1)[1] == "on"
    rows, phases, space = run(traj, alpha, theta, domain_of(sys.argv[2]), context)
    with open(sys.argv[3], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else repr(r[c]) if isinstance(r.get(c), float) else r[c])
                        for c in COLUMNS})
    json.dump(dict(space=space, phases=phases), open(sys.argv[4], "w"), indent=1)
    loaded = [m for m in ("shared.recognizer", "shared.likelihood_functions") if m in sys.modules]
    assert not loaded, f"the independence boundary is broken: {loaded} loaded"
    print(f"{traj['scenario']}: {len(rows)} rows; hypotheses {space}; independence: neither recognizer module loaded")
