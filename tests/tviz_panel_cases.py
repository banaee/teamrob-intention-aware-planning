"""
tests/tviz_panel_cases.py

T-viz 1a (iv): panel 4a's reference cases (design_records.md, "T-viz, the web-ui", 1a, THE PANELS' CONTENT, item 6), run
through Mesa's piece, for the page's test of the script lines (webui/page/test/script.test.ts). For each case: the
human's script, the tick updates' human activity in order, and per tick the true state of every script line, read from
the human executor's own state (its frames, its closed entries, the record's transitions by object identity), not from
the messages. The page derives the states from the messages; the test compares the two.

    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python -m tests.tviz_panel_cases     # rewrites the fixtures

The fixtures live under tests/fixtures/tviz_panel/ (outside webui/: they name a domain's tasks and objects).
tests/test_tviz_panel.py checks that they are what this module makes now.
"""

import json
import os
from pathlib import Path

from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator
from webui import messages as m
from world import record as rec
from world.record import ClosingRef, OrdinaryRef, RepeatableRef

FIXTURES = Path(__file__).parent / "fixtures" / "tviz_panel"
# (name, domain, scenario): a task in progress and an interruption after an action (scenario_s02_02), an interruption
# inside an action (scenario_s09_13, scenario_s06_09), resumptions (all four; scenario_s11_03 an office break).
CASES = [("kitting_s02_02", "kitting", "scenario_s02_02"), ("kitting_s09_13", "kitting", "scenario_s09_13"),
         ("dock_loading_s06_09", "dock_loading", "scenario_s06_09"),
         ("dock_loading_s11_03", "dock_loading", "scenario_s11_03")]
MAX_STEPS = 800
_OUTCOME = {rec.Outcome.COMPLETED: "completed", rec.Outcome.ABANDONED: "abandoned",
            rec.Outcome.INFEASIBLE: "infeasible"}
_PART = {OrdinaryRef: "ordinary", RepeatableRef: "repeatable", ClosingRef: "closing"}


def _key(ref) -> str:
    return f"{_PART[type(ref)]} {ref.index}"


class _Truth:
    """Per tick, every script line's state from the executor's own state."""

    def __init__(self, machine):
        self.machine = machine
        self.refs = ([OrdinaryRef(i) for i in range(len(machine.entries))]
                     + [RepeatableRef(i) for i in range(len(machine.repeatable))]
                     + [ClosingRef(j) for j in range(len(machine.closing))])
        self.frames = []                 # (frame, its entry) seen on the stack
        self.outcome = {}                # entry key -> outcome word
        self.event_outcome = {}          # event key -> outcome word
        self.fired, self.unfired = set(), set()

    def _events(self):
        for ref in self.refs:
            if isinstance(ref, RepeatableRef):
                continue
            entry = self.machine.entries[ref.index] if isinstance(ref, OrdinaryRef) else self.machine.closing[ref.index]
            for k, ev in enumerate(entry.events):
                yield ref, k, ev

    def tick(self, transitions) -> dict:
        machine = self.machine
        for frame in machine.stack:
            if not any(f is frame for f, _ in self.frames):
                self.frames.append((frame, frame.entry))
        for t in transitions:
            if isinstance(t, rec.Left) and t.outcome is not rec.Outcome.SUSPENDED:
                frame = next((f for f, _ in self.frames if f.task is t.task), None)
                if frame is not None and frame.entry is not None:
                    self.outcome[_key(frame.entry)] = _OUTCOME[t.outcome]
                for ref, k, ev in self._events():
                    if ev.decision.__class__.__name__ == "Start" and ev.decision.task is t.task:
                        self.event_outcome[f"{_key(ref)} {k}"] = _OUTCOME[t.outcome]
            for ref, k, ev in self._events():
                if isinstance(t, rec.Started) and t.trigger is ev.trigger:
                    self.fired.add(f"{_key(ref)} {k}")
                if isinstance(t, rec.Unfired) and t.event is ev:
                    self.unfired.add(f"{_key(ref)} {k}")
        stack = list(reversed(machine.stack))          # top first
        state = {}
        for ref in self.refs:
            at = next((i for i, f in enumerate(stack) if f.entry == ref), None)
            closed = (isinstance(ref, OrdinaryRef) and machine.closed[ref.index]) or \
                     (isinstance(ref, ClosingRef) and ref.index < machine.closing_done)
            state[f"entry {_key(ref)}"] = ("in progress" if at == 0 else "suspended" if at is not None
                                           else self.outcome[_key(ref)] if closed else "open")
        for ref, k, ev in self._events():
            key = f"{_key(ref)} {k}"
            starts = ev.decision.__class__.__name__ == "Start"
            if key in self.unfired:
                word = "unfired"
            elif not starts:
                word = "fired" if state[f"entry {_key(ref)}"] == "abandoned" else "pending"
            elif stack and stack[0].task is ev.decision.task:
                word = "in progress"
            elif key in self.event_outcome:
                word = self.event_outcome[key]
            else:
                word = "fired" if key in self.fired else "pending"
            state[f"event {key}"] = word
        return state


def run_case(domain: str, scenario: str) -> dict:
    """The case run through the piece until all agents have finished (or MAX_STEPS): the script, the activity per tick
    update, and the truth per tick update. Its log pair is removed."""
    before = set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
    side = simulator.build(m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario,
                                          options=catalogue.default_choice.options), "case")
    human_id = side.description.world.humans[0].id
    human = side._model.humans[human_id]
    truth = _Truth(human.machine)
    activity = lambda u: next(a for a in u.world.activity if a.human == human_id)
    ticks = [dict(tick=None, activity=json.loads(activity(side.state()).model_dump_json()))]
    states = [truth.tick(())]
    for _ in range(MAX_STEPS):
        update = side.step()
        ticks.append(dict(tick=update.tick, activity=json.loads(activity(update).model_dump_json())))
        states.append(truth.tick(human.record.transitions_at(update.tick)))
        if update.run.finished_at is not None:
            break
    side.end(m.EndReason.RESET)
    for name in sorted(set(os.listdir(LOG_DIR)) - before):
        os.remove(os.path.join(LOG_DIR, name))
    script = next(s for s in side.description.world.scripts if s.human == human_id)
    # Kept: the ticks on which what the page's derivation reads changes (the transitions, the stack's entries, the open
    # entries, the tag); the truth must not change on a tick that is dropped. The action in hand is not read.
    read = lambda a: (a["transitions"], a["stack_entries"], a["open_entries"], a["tag"])
    kept_ticks, kept_states = [], []
    for i, (u, s) in enumerate(zip(ticks, states)):
        if i == 0 or u["activity"]["transitions"] or read(u["activity"]) != read(ticks[i - 1]["activity"]):
            u["activity"].pop("action")
            kept_ticks.append(u)
            kept_states.append(s)
        elif s != kept_states[-1]:
            raise AssertionError(f"{scenario}: the truth changed at tick {u['tick']} with nothing the page reads")
    return dict(domain=domain, scenario=scenario, script=json.loads(script.model_dump_json()), ticks=kept_ticks,
                truth=kept_states)


def main() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    for name, domain, scenario in CASES:
        (FIXTURES / f"{name}.json").write_text(json.dumps(run_case(domain, scenario), separators=(",", ":")) + "\n")
        print("[tviz_panel_cases] wrote", FIXTURES / f"{name}.json")


if __name__ == "__main__":
    main()
