#!/usr/bin/env python3
"""
chain.py — the meta-planner test-bed's chain assembly (MPB-1): the expected (tick, trigger, cause) chain, with the
gate, leader and projection at each decision, assembled at the compare step from the oracle's per-tick table
(expected_ticks.json) and the run's observed no_current_task ticks. It imports nothing of the planner (mpblib and the
standard library only).

    chain.py <expected_ticks.json> <observed.json> <expected_decisions.json>

observed.json (actual.py): the run's no_current_task ticks, its terminal tick (the no_current_task decision whose
update returned no task; null when the run did not complete) and the comparison horizon.

The rules, with their sources (IO = shared/io_contracts.md §2.2; DD = design_decisions.md):
  C1 The decision record: the hypothesis the last decision was projected against (set when admission builds a
     projection, cleared otherwise) and the tick its fallback ends (set when admission returns a fallback, cleared
     otherwise); set at every decision, the robot's included (DD D2; DD "T-D P", Q6; MPB-1).
  C2 On a tick: no_current_task, then recognition_changed, then projection_expired; a no_current_task tick masks the
     others (DD D3 as superseded by Q6; IO).
  C3 recognition_changed, with a record: REPLACED (most_likely is no longer it), then BOUNDARY (the belief re-initialised
     at an episode boundary on this tick), then RETRACTION (the recorded hypothesis's hypothesis adequacy is inadequate);
     without one: ENTERED (the gate clears) (IO, L-build; DD "T-D L", L2 (ii), L5 B; D2).
  C4 projection_expired: a fallback end is recorded and the tick is at or after it (IO; DD Q6).
  C5 On a fired trigger admission is asked once: the gate clears, the leader's plan is admitted; otherwise the fallback
     (IO, update_human_projection; DD "T-D P", P4).
  C6 After the terminal decision nothing is evaluated (DD "The cognitive loop does not end with the task pool").
"""
import json
import sys
from typing import List, Optional, Set

from mpblib import Cause, Decision, Gate, TickRow, Trigger, dump, load_ticks


def assemble(ticks: List[TickRow], nct: Set[int], terminal: Optional[int], horizon: int) -> List[Decision]:
    recorded: Optional[str] = None
    expiry: Optional[float] = None
    out: List[Decision] = []
    for row in sorted(ticks, key=lambda r: r.tick):
        t = row.tick
        if t >= horizon or (terminal is not None and t > terminal):         # C6
            break
        trigger, cause = None, None
        if t in nct:                                                          # C2
            trigger = Trigger.NO_CURRENT_TASK
        else:
            if recorded is not None:                                          # C3
                if row.leader != recorded:
                    cause = Cause.REPLACED
                elif row.boundary:
                    cause = Cause.BOUNDARY
                elif row.adequacy.get(recorded) == "inadequate":
                    cause = Cause.RETRACTION
            elif row.gate is Gate.CLEARS:
                cause = Cause.ENTERED
            if cause is not None:
                trigger = Trigger.RECOGNITION_CHANGED
            elif expiry is not None and t >= expiry:                          # C4
                trigger = Trigger.PROJECTION_EXPIRED
        if trigger is None:
            continue
        if row.gate is Gate.CLEARS:                                           # C5, C1
            recorded, expiry = row.leader, None
            out.append(Decision(t, trigger, cause, row.gate, row.leader, row.warrant, row.admitted, None))
        else:
            recorded = None
            expiry = None if row.fallback is None else row.fallback.end
            out.append(Decision(t, trigger, cause, row.gate, row.leader, (), None, row.fallback))
    return out


if __name__ == "__main__":
    ticks = load_ticks(sys.argv[1])
    obs = json.load(open(sys.argv[2]))
    decisions = assemble(ticks, set(obs["no_current_task"]), obs["terminal"], obs["horizon"])
    dump(decisions, sys.argv[3])
    print(f"chain: {len(decisions)} decisions, "
          f"{sum(d.trigger is not Trigger.NO_CURRENT_TASK for d in decisions)} of them not no_current_task")
