#!/usr/bin/env python3
"""
generate.py — writes the setups and scenarios of the demo-day round of T-F (Hadi, 8 October 2026; README.md beside this
file): five setups env_setup_100 to env_setup_104 on env_layout_100, ten scenarios each (scenario_sNNN_01 to _10), as
ordinary files a person reads: domains/kitting/setups/env_setup_NNN.json and domains/kitting/scenarios/scenarios_sNNN.py.
Run once, before any run; its outputs are committed before the first run and never redrawn after a result is seen.

    generate.py          draws, checks each scenario with the loader's own check, writes the files

THE DRAWS (one stream, random.Random(SEED), in the order below; every rule stated before the first draw):
- Per setup, in order 100 to 104: each item_k (k = 1..24) on shelf_k, its destination kitting_table_0 or
  kitting_table_1 with equal chance (k in order); then the start s of the timeline's one window, break_time [s, s + 100),
  an integer uniform on [0, 200] (the window starts while the shortest script, three deliveries, is still at work).
- Per scenario, in order _01 to _10 of the setup: the robot's count n_r uniform on 8..13, the human's count n_h uniform on
  3..7; then n_r + n_h distinct items drawn without replacement from the 24, the first n_r the robot's pool in that
  order, the rest the human's deliveries in that order (disjoint by construction). Then the group's additions:
  a  (_01, _02)  the deliveries only.
  b  (_03 to _06) one coffee_break("coffee_machine_1") at a place.
  c  (_07, _08)  the mix: one switch mid-task (a change of mind to another of the human's deliveries), one coffee break at
                 a place, one unmodelled behaviour; drawn in that order.
     (_09, _10)  unmodelled behaviour only: two unmodelled behaviours, drawn one after the other.
- A place (for a coffee break, a stand, a walk to the corner and a stand there): between entries or inside a delivery,
  each with chance 1/2; between: one of the n + 1 slots before a delivery entry or before the exit walk, uniform; inside:
  one of the delivery entries that carries no event and is not misdelivered, uniform, then one of its three anchors,
  uniform: after the walk to the shelf (`.at(move_to, ..., occurrence=0)`), after the grasp (`.at(pick_up, ...)`), after
  the carry to the table (`.at(move_to, ..., occurrence=1)`). Two additions in one slot keep their draw order.
- The switch: one delivery entry A, uniform; another delivery B, uniform among the rest, taken out of the entries and
  started from A at one of two anchors, uniform: after A's walk to the shelf, after A's grasp (B is then expanded with
  A's item in hand, deliver_with_return); A resumes after B.
- An unmodelled behaviour (glossary §7, label B; §6, deviation): its kind uniform among three:
    stand            stand(d) at a place: the human stands still where it is (TASK_ABSENT);
    corner           go_to_and_stand("corner_SE", d) at a place: a walk to the corner and a stand there (TASK_ABSENT);
    misdelivery      one delivery entry, uniform among those that carry no event and are not misdelivered, delivered to
                     the other table (BINDING_ABSENT; the assigned task keeps its designated table).
  d uniform among PT40S, PT60S, PT80S, PT120S (20 to 60 ticks; step 5e's durations).
- Every script ends with the exit walk go_to("corner_SE") (docs/assumptions.md 1.1). The human is assigned every
  delivery it performs, at its designated table; the robot is assigned its pool and observes the human.
- Starts, fixed: the human at (5, 380), before kitting_table_0; the robot at (0, -380), before kitting_table_1.

THE CHECK AND THE REDRAW RULE: each scenario's source is rendered, executed into its ScenarioConfig and built by the
loader (mesa_sim/run_config.py, build_model: the load-time replay and every load check) before the next draw. A draw that
cannot be placed (no free delivery entry for an addition) or that the loader refuses is discarded whole, and the
scenario is drawn again from the continuing stream; the count of discarded draws is printed and written in the module's
docstring. The model built for the check is never stepped, so it writes no log.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim")]

SEED = 20261008
LAYOUT = "env_layout_100"
SETUPS = [100, 101, 102, 103, 104]
TABLES = ("kitting_table_0", "kitting_table_1")
N_ITEMS = 24
WINDOW = 100
WINDOW_START = (0, 200)
DURATIONS = ("PT40S", "PT60S", "PT80S", "PT120S")
HUMAN_START, ROBOT_START = (5, 380), (0, -380)
GROUPS = ["a", "a", "b", "b", "b", "b", "c_mix", "c_mix", "c_unmodelled", "c_unmodelled"]
ANCHORS = [("move_to", 0, "after the walk to the shelf"), ("pick_up", None, "after the grasp"),
           ("move_to", 1, "after the carry to the table")]
SWITCH_ANCHORS = ANCHORS[:2]
PURPOSE = {
    "a": "group a: the human does its assigned deliveries only",
    "b": "group b: the assigned deliveries and one coffee break",
    "c_mix": "group c, the mix: a switch mid-task, a coffee break and an unmodelled behaviour",
    "c_unmodelled": "group c, unmodelled behaviour only: two unmodelled behaviours",
}


class Invalid(Exception):
    """A draw that cannot be placed; discarded whole (the redraw rule)."""


class Entry:
    """A delivery entry of the human's script: its item, the table it is delivered to, at most one event."""

    def __init__(self, item, designated):
        self.item, self.designated, self.table, self.event = item, designated, designated, None

    def free(self):
        return self.event is None and self.table == self.designated


def task_src(kind, arg=None):
    return {"coffee": 'coffee_break("coffee_machine_1")', "stand": f'stand("{arg}")',
            "corner": f'go_to_and_stand("corner_SE", "{arg}")'}[kind]


def task_words(kind, arg=None):
    return {"coffee": "a coffee break", "stand": f"a stand of {arg}",
            "corner": f"a walk to corner_SE and a stand of {arg} there"}[kind]


def place(rng, entries, slots, src, words, notes):
    """Puts the task `src` at a place (the module's rule): between entries or inside a free delivery entry."""
    if rng.random() < 0.5:
        k = rng.randrange(len(entries) + 1)
        slots[k].append(src)
        notes.append(f"{words} " + (f"before delivery {k + 1}" if k < len(entries) else "before the exit walk"))
        return
    free = [e for e in entries if e.free()]
    if not free:
        raise Invalid("no free delivery entry")
    e = rng.choice(free)
    action, occ, where = rng.choice(ANCHORS)
    e.event = (action, occ, src)
    notes.append(f"{words} inside the delivery of {e.item}, {where}")


def unmodelled(rng, entries, slots, notes):
    kind = rng.choice(["stand", "corner", "misdelivery"])
    if kind == "misdelivery":
        free = [e for e in entries if e.free()]
        if not free:
            raise Invalid("no free delivery entry")
        e = rng.choice(free)
        e.table = TABLES[1 - TABLES.index(e.designated)]
        notes.append(f"the misdelivery of {e.item} to {e.table} (designated {e.designated})")
        return
    d = rng.choice(DURATIONS)
    place(rng, entries, slots, task_src(kind, d), task_words(kind, d), notes)


def draw_scenario(rng, group, dest):
    n_r, n_h = rng.randint(8, 13), rng.randint(3, 7)
    items = rng.sample(range(1, N_ITEMS + 1), n_r + n_h)
    robot = [f"item_{k}" for k in items[:n_r]]
    entries = [Entry(f"item_{k}", dest[f"item_{k}"]) for k in items[n_r:]]
    assigned = [(e.item, e.designated) for e in entries]
    slots = [[] for _ in range(len(entries) + 1)]
    notes = []
    if group == "b":
        place(rng, entries, slots, task_src("coffee"), task_words("coffee"), notes)
    elif group == "c_mix":
        a = rng.choice(entries)
        b = rng.choice([e for e in entries if e is not a])
        action, occ, where = rng.choice(SWITCH_ANCHORS)
        entries.remove(b)
        slots.pop()   # no addition is placed yet: one slot fewer, all empty
        a.event = (action, occ, f'deliver_item("{b.item}", table="{b.designated}")')
        notes.append(f"the switch from the delivery of {a.item} to the delivery of {b.item}, {where}; "
                     f"{a.item}'s delivery resumes after it")
        place(rng, entries, slots, task_src("coffee"), task_words("coffee"), notes)
        unmodelled(rng, entries, slots, notes)
    elif group == "c_unmodelled":
        unmodelled(rng, entries, slots, notes)
        unmodelled(rng, entries, slots, notes)
    return dict(n_r=n_r, n_h=n_h, robot=robot, entries=entries, slots=slots, assigned=assigned, notes=notes)


def render_entry(e):
    s = f'deliver_item("{e.item}", table="{e.table}")'
    if e.event is not None:
        action, occ, src = e.event
        s += f".at({action}, {src}" + (f", occurrence={occ})" if occ is not None else ")")
    return s


def render_scenario(sid, setup, group, d, dest):
    lines = []
    for k, e in enumerate(d["entries"]):
        lines += d["slots"][k] + [render_entry(e)]
    lines += d["slots"][-1] + ['go_to("corner_SE")']
    script = "".join(f"                {l},\n" for l in lines)
    assigned = "".join(f'                deliver_item("{i}", table="{t}"),\n' for i, t in d["assigned"])
    pool = "".join(f'                deliver_item("{i}", table="{dest[i]}"),\n' for i in d["robot"])
    contents = "; ".join(d["notes"]) if d["notes"] else "nothing besides the deliveries"
    description = (f"{sid}: {PURPOSE[group]}. The robot has {d['n_r']} deliveries, the human {d['n_h']}; the human's "
                   f"script: {contents}; then the exit walk. Generated by analysis/kitting/tf_demo/generate.py "
                   f"(seed {SEED}).")
    return (f'{sid} = ScenarioConfig(\n'
            f'    id="{sid}",\n'
            f'    setup="{setup}",\n'
            f'    reference_layouts=["{LAYOUT}"],\n'
            f'    description=(\n        {json.dumps(description)}\n    ),\n'
            f'    agents=[\n'
            f'        AgentConfig(\n'
            f'            agent_id="human_0",\n'
            f'            agent_type="human",\n'
            f'            start_position={HUMAN_START},\n'
            f'            scheduled_tasks=Script([\n{script}            ]),\n'
            f'            assigned_tasks=[\n{assigned}            ],\n'
            f'            observes=[],\n'
            f'        ),\n'
            f'        AgentConfig(\n'
            f'            agent_id="robot_0",\n'
            f'            agent_type="robot",\n'
            f'            start_position={ROBOT_START},\n'
            f'            assigned_tasks=[\n{pool}            ],\n'
            f'            observes=["human_0"],\n'
            f'        ),\n'
            f'    ],\n'
            f')\n')


IMPORTS = ("from shared.types import AgentConfig, ScenarioConfig, Script\n"
           "from domains.kitting.actions import move_to, pick_up\n"
           "from domains.kitting.script import deliver_item, coffee_break, go_to, stand, go_to_and_stand\n")


def check(src, sid, setup, setup_path):
    """The loader's check of one scenario: its source executed, registered in memory, built (never stepped)."""
    from mesa_sim.run_config import DOMAIN_REGISTRY, build_model
    ns = {}
    exec(IMPORTS + src, ns)
    domain = DOMAIN_REGISTRY["kitting"]
    domain["setups"][setup] = str(setup_path)
    domain["scenarios"][sid] = ns[sid]
    try:
        build_model(dict(domain="kitting", layout=LAYOUT, scenario=sid))
    finally:
        del domain["scenarios"][sid]


def setup_json(setup, dest, start):
    objs = [dict(id=f"item_{k}", type="item", initial_container=f"shelf_{k}", destination=dest[f"item_{k}"],
                 size=[25, 25], notes=f"On shelf_{k}; its destination drawn (generate.py, seed {SEED}).")
            for k in range(1, N_ITEMS + 1)]
    return dict(notes=(f"{setup}: the demo-day round of T-F (analysis/kitting/tf_demo/), on {LAYOUT}. Each shelf_k holds "
                       f"item_k; each destination drawn between kitting_table_0 and kitting_table_1; one timeline fact, "
                       f"break_time over [{start}, {start + WINDOW}), its start drawn. Generated by "
                       f"analysis/kitting/tf_demo/generate.py (seed {SEED})."),
                timeline=[dict(fact="break_time", **{"from": start, "until": start + WINDOW})],
                env_objects=objs)


def main():
    import logging
    logging.disable(logging.CRITICAL)
    rng = random.Random(SEED)
    summary = []
    for n in SETUPS:
        setup = f"env_setup_{n}"
        dest = {f"item_{k}": rng.choice(TABLES) for k in range(1, N_ITEMS + 1)}
        start = rng.randint(*WINDOW_START)
        setup_path = ROOT / "domains" / "kitting" / "setups" / f"{setup}.json"
        setup_path.write_text(json.dumps(setup_json(setup, dest, start), indent=2) + "\n")
        sources, discarded = [], []
        for j, group in enumerate(GROUPS, 1):
            sid = f"scenario_s{n}_{j:02d}"
            while True:
                try:
                    d = draw_scenario(rng, group, dest)
                    src = render_scenario(sid, setup, group, d, dest)
                    check(src, sid, setup, setup_path)
                    break
                except Exception as e:   # Invalid, or the loader's refusal: the draw is discarded whole
                    discarded.append(f"{sid}: {type(e).__name__}: {e}")
            sources.append(src)
            summary.append((sid, group, d["n_r"], d["n_h"], d["notes"]))
        doc = (f'# domains/kitting/scenarios/scenarios_s{n}.py\n"""\n'
               f"Kitting scenarios on {setup}: the demo-day round of T-F (Hadi, 8 October 2026; "
               f"analysis/kitting/tf_demo/README.md), on {LAYOUT}. One module per setup. GENERATED by "
               f"analysis/kitting/tf_demo/generate.py (seed {SEED}); not edited by hand, never redrawn after a result.\n"
               f"_01, _02 group a (deliveries only); _03 to _06 group b (one coffee break); _07, _08 group c, the mix (a "
               f"switch mid-task, a coffee break, an unmodelled behaviour); _09, _10 group c, unmodelled behaviour only.\n"
               f"The robot's and the human's items are disjoint. Every script ends with the exit walk to corner_SE.\n"
               f"Draws discarded by the redraw rule: {len(discarded)}"
               + "".join(f"\n- {x}" for x in discarded) + '\n"""\n\n')
        (ROOT / "domains" / "kitting" / "scenarios" / f"scenarios_s{n}.py").write_text(
            doc + IMPORTS + "\n\n" + "\n\n".join(sources))
        print(f"{setup}: break_time [{start}, {start + WINDOW}); discarded draws {len(discarded)}")
        for x in discarded:
            print(f"  {x}")
    for sid, group, n_r, n_h, notes in summary:
        print(f"{sid} {group:13s} robot {n_r:2d} human {n_h} | {'; '.join(notes)}")


if __name__ == "__main__":
    main()
