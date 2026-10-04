"""
The meta-planner test-bed's instrument (analysis/instruments/mpb/ and analysis/kitting/mpb/; design_records.md, "The meta-planner test-bed (MPB)"): its own
derivations (P4's perception facts, the fallback's ray, its end and expiry), the chain assembly and the compare, on
synthetic inputs derived from the records (T-D P, P4 and Q6; shared/io_contracts.md §2.2; D2, D3, T-D L); none from a
run. And the oracle's independence boundary (MPB-1).
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MPB = ROOT / "analysis" / "instruments" / "mpb"
sys.path.insert(0, str(MPB))
sys.path.insert(0, str(ROOT / "analysis" / "kitting" / "mpb"))     # horizon.py and properties.py, kitting's

from mpblib import (Action, Admitted, Cause, Decision, Fallback, Gate, Mode, Perception, Room, TickRow, Trigger,
                    fallback, perception, reach)
from chain import assemble
from compare import compare_decisions, compare_ticks, log_text
from horizon import _arrival

ROOM = Room(-500.0, 500.0, -700.0, 700.0, {"table": (0.0, 220.0), "door": (300.0, 690.0)}, 30.0)


# ---- P4's perception facts (glossary §9; T-D P, P4) -------------------------------------------------------------
def test_a_straight_walk_with_rounding_level_jitter_is_one_run():
    pos = [(0.0, 0.0)] + [(0.0, 20.0 * i + (1e-15 if i % 2 else 0.0)) for i in range(1, 6)]
    runs = [p.run_length for p in perception(pos)[1:]]
    assert runs == [1, 2, 3, 4, 5]


def test_a_turn_starts_a_run_of_one_and_a_stop_ends_it():
    pos = [(0.0, 0.0), (0.0, 20.0), (0.0, 40.0), (20.0, 40.0), (20.0, 40.0), (20.0, 40.0), (40.0, 40.0)]
    p = perception(pos)
    assert p[0] is None                                             # no previous observation
    assert [x.run_length for x in p[1:]] == [1, 2, 1, 0, 0, 1]
    assert [x.standing_count for x in p[1:]] == [0, 0, 0, 1, 2, 0]
    assert p[4].displacement == (0.0, 0.0)


# ---- the ray (P2 as kept by P4) -------------------------------------------------------------------------------
def test_the_ray_stops_at_the_wall():
    assert reach((0.0, 0.0), (1.0, 0.0), ROOM) == pytest.approx(500.0)


def test_the_ray_stops_where_it_enters_the_first_objects_radius():
    assert reach((0.0, 0.0), (0.0, 1.0), ROOM) == pytest.approx(190.0)          # table at 220, radius 30


def test_an_object_whose_radius_contains_the_start_is_skipped():
    assert reach((0.0, 200.0), (0.0, 1.0), ROOM) == pytest.approx(500.0)        # through the table to the wall


def test_an_object_behind_or_beside_the_ray_is_ignored_and_a_landmark_counts():
    assert reach((0.0, 300.0), (0.0, 1.0), ROOM) == pytest.approx(400.0)        # the table behind: to the wall
    assert reach((300.0, 300.0), (0.0, 1.0), ROOM) == pytest.approx(360.0)      # the landmark door at 690
    assert reach((340.0, 300.0), (0.0, 1.0), ROOM) == pytest.approx(400.0)      # 40 cm beside it: missed


# ---- the fallback's shape, end and expiry (P4, Q6) -------------------------------------------------------------
def test_a_stand_of_k_ticks_projects_k_ticks_from_the_offset():
    f = fallback(14, (0.0, 0.0), Perception((0.0, 0.0), 0, 15), ROOM, 1.0)
    assert (f.mode, f.k, f.duration, f.end, f.expiry_tick()) == (Mode.STANDING, 15, 15.0, 30.0, 30)


def test_a_run_of_k_ticks_projects_k_ticks_unless_cut():
    free = fallback(6, (0.0, -400.0), Perception((0.0, 20.0), 7, 0), ROOM, 1.0)
    assert (free.mode, free.k, free.duration, free.end) == (Mode.MOVING, 7, 7.0, 14.0)
    cut = fallback(14, (0.0, 0.0), Perception((0.0, 20.0), 15, 0), ROOM, 1.0)
    assert cut.duration == pytest.approx(9.5) and cut.expiry_tick() == math.ceil(14 + 1 + 9.5)


def test_no_previous_observation_no_fallback():
    assert fallback(0, (0.0, 0.0), None, ROOM, 1.0) is None


# ---- the chain (C1 to C6: D2, D3, Q6, L2 (ii), L5 B, io_contracts §2.2) -------------------------------------------
A = Admitted("h(?x=a)", (Action("move_to", (("?target", "t"),)),))
FB = lambda t, n: Fallback(Mode.STANDING, n, float(n), t + 1.0 + n)


def row(t, leader="h(?x=a)", gate=Gate.BELOW_THETA, boundary=False, adequacy="adequate", fb=None):
    return TickRow(t, leader, boundary, "adequate", gate, {leader: adequacy} if leader else {}, {}, (),
                   None, fb if fb is not None else FB(t, 1), A if gate is Gate.CLEARS else None)


def chain(rows, nct=(0,), terminal=None, horizon=100):
    return [(d.tick, d.trigger.value, d.cause and d.cause.value) for d in assemble(rows, set(nct), terminal, horizon)]


def test_entered_on_the_first_clearing_and_retention_by_identity_through_a_dip():
    rows = [row(0, fb=FB(0, 50)), row(1, gate=Gate.CLEARS), row(2), row(3, gate=Gate.CLEARS)]
    assert chain(rows) == [(0, "no_current_task", None), (1, "recognition_changed", "entered")]


def test_replaced_before_boundary_and_boundary_when_the_leader_stays():
    rows = [row(0, gate=Gate.CLEARS), row(1, leader="h(?x=b)", boundary=True, fb=FB(1, 50))]
    assert chain(rows)[-1] == (1, "recognition_changed", "replaced")
    rows = [row(0, gate=Gate.CLEARS), row(1, boundary=True, gate=Gate.LEADER_NO_OBSERVATION, fb=FB(1, 50))]
    assert chain(rows)[-1] == (1, "recognition_changed", "boundary")


def test_retraction_reads_the_recorded_hypothesis_only():
    rival = TickRow(1, "h(?x=a)", False, "adequate", Gate.CLEARS, {"h(?x=a)": "adequate", "h(?x=b)": "inadequate"}, {},
                    (), None,
                    None, A)
    assert chain([row(0, gate=Gate.CLEARS), rival]) == [(0, "no_current_task", None)]
    rows = [row(0, gate=Gate.CLEARS), row(1, gate=Gate.LEADER_INADEQUATE, adequacy="inadequate", fb=FB(1, 50))]
    assert chain(rows)[-1] == (1, "recognition_changed", "retraction")


def test_the_expiry_fires_on_the_first_tick_at_or_after_the_fallbacks_end_and_yields_to_recognition():
    rows = [row(0, fb=Fallback(Mode.MOVING, 1, 1.0, 2.0))] + [row(t, fb=FB(t, 50)) for t in (1, 2, 3)]
    assert chain(rows) == [(0, "no_current_task", None), (2, "projection_expired", None)]
    rows = [row(0, fb=FB(0, 1)), row(1), row(2, gate=Gate.CLEARS)]
    assert chain(rows) == [(0, "no_current_task", None), (2, "recognition_changed", "entered")]


def test_no_current_task_masks_the_others_and_nothing_follows_the_terminal_decision():
    rows = [row(0, fb=FB(0, 50)), row(1, gate=Gate.CLEARS), row(2, gate=Gate.CLEARS)]
    assert chain(rows, nct=(0, 1)) == [(0, "no_current_task", None), (1, "no_current_task", None)]
    rows = [row(0, fb=FB(0, 50)), row(1, gate=Gate.CLEARS)]
    assert chain(rows, nct=(0,), terminal=0) == [(0, "no_current_task", None)]


# ---- the compare ---------------------------------------------------------------------------------------------
def test_identical_sides_agree_and_one_altered_cell_is_one_disagreement():
    exp = [row(0, gate=Gate.CLEARS), row(1)]
    act = [dict(tick=0, leader="h(?x=a)", boundary=False, finding="adequate", gate="clears",
                adequacy={"h(?x=a)": "adequate"}, observation_warrant={}, evaluated=False, perception=None),
           dict(tick=1, leader="h(?x=a)", boundary=False, finding="adequate", gate="none(below_theta)",
                adequacy={"h(?x=a)": "adequate"}, observation_warrant={}, evaluated=False, perception=None)]
    assert compare_ticks(exp, act, 10)[1] == []
    act[1]["gate"] = "clears"
    bad = compare_ticks(exp, act, 10)[1]
    assert [(t, c) for t, c, _, _ in bad] == [(1, "gate")]
    act[1]["gate"], act[0]["finding"] = "none(below_theta)", "unexplained"
    assert [(t, c) for t, c, _, _ in compare_ticks(exp, act, 10)[1]] == [(0, "finding")]


# ---- X5's ground (1), measured (T-D X, X5) -------------------------------------------------------------------
def test_x5_ground1_needs_an_unexplained_finding_outliving_a_refused_re_decision():
    from properties import x5_ground1
    ticks = [dict(tick=t, finding=f) for t, f in enumerate(
        ["adequate", "unexplained", "unexplained", "unexplained", "adequate", "unexplained", "unexplained"])]
    refused = lambda t: Decision(t, Trigger.PROJECTION_EXPIRED, None, Gate.LEADER_INADEQUATE, "h", (), None, FB(t, 1))
    admitted = Decision(5, Trigger.RECOGNITION_CHANGED, Cause.ENTERED, Gate.CLEARS, "h", ("observation",), A, None)
    out = x5_ground1(ticks, [refused(2), admitted])
    assert out == [dict(first=1, last=3, refused_decisions=[2], ground1_from=3),
                   dict(first=5, last=6, refused_decisions=[], ground1_from=None)]
    assert x5_ground1(ticks, [refused(3)])[0]["ground1_from"] is None     # nothing after the re-decision


def test_a_missing_decision_and_a_different_fallback_are_disagreements():
    e = [Decision(2, Trigger.PROJECTION_EXPIRED, None, Gate.BELOW_THETA, "h", (), None, FB(2, 3))]
    a = [Decision(2, Trigger.PROJECTION_EXPIRED, None, Gate.BELOW_THETA, "h", (), None, FB(2, 4))]
    assert [w for _, w, _, _ in compare_decisions(e, a)[1]] == ["part 3"]
    assert [w for _, w, _, _ in compare_decisions(e, [])[1]] == ["part 1"]


def test_the_log_text_a_decision_implies():
    built = Decision(1, Trigger.RECOGNITION_CHANGED, Cause.ENTERED, Gate.CLEARS, "h", ("observation",), A, None)
    assert log_text(built) == "built warrant=observation"          # the only source since AM67 (D2)
    assert log_text(Decision(3, Trigger.NO_CURRENT_TASK, None, Gate.LEADER_OUTRANKED, "h", (), None, FB(3, 2))) \
        == "fallback refused=none(leader_outranked)"
    assert log_text(Decision(2, Trigger.RECOGNITION_CHANGED, Cause.REPLACED, Gate.LEADER_NO_OBSERVATION, "h", (), None,
                             FB(2, 2))) == "fallback refused=none(leader_no_observation)"


def test_the_safety_caps_arrival_point_is_the_radius_short_of_the_target():
    assert _arrival((0.0, 0.0), (0.0, 100.0), 30.0) == pytest.approx((0.0, 70.0))
    assert _arrival((0.0, 90.0), (0.0, 100.0), 30.0) == (0.0, 90.0)


# ---- the independence boundary (MPB-1) -------------------------------------------------------------------------
def test_the_oracle_loads_nothing_of_the_planner_the_recognizer_the_projection_or_the_body():
    code = ("import sys; sys.path.insert(0, %r); import mpb_oracle; "
            "print([m for m in sys.modules if m in mpb_oracle.FORBIDDEN or m.startswith('mesa_sim')])" % str(MPB))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=ROOT,
                         env=dict(PYTHONHASHSEED="0", PATH="/usr/bin:/bin"))
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip().splitlines()[-1] == "[]"


# ---- the gate rulings' build (AM68, AM75, AM76; D3) ---------------------------------------------------------------
def test_the_irb_oracles_rank_is_exact_beyond_its_agreement_level_and_undetermined_within_it():
    sys.path.insert(0, str(ROOT / "analysis" / "instruments" / "irb"))
    from oracle import rank, UNDETERMINED
    assert rank({"a": 0.6, "b": 0.4}, "b") == "outranked" and rank({"a": 0.6, "b": 0.4}, "a") == "not_outranked"
    assert rank({"a": 0.5, "b": 0.5}, "a") == "not_outranked"                   # an exact tie passes (D3 amended)
    assert rank({"a": 0.5, "b": 0.5, "c": 0.0}, "c") == "outranked"
    assert rank({"a": 0.5 + 1e-12, "b": 0.5 - 1e-12}, "b") == UNDETERMINED      # within 1e-9: not decided here
    assert rank({"a": 0.5, "b": 0.3, "c": 0.2}, "c") == "outranked"


def test_the_chain_stops_on_an_undetermined_gate_it_asks():
    # D3: an undetermined gate on a tick the chain asks it is not guessed
    with pytest.raises(SystemExit):
        assemble([row(0, gate=Gate.UNDETERMINED)], {0}, None, 100)
    # not asked (a record stands and nothing fires): no stop
    rows = [row(0, gate=Gate.CLEARS), row(1, gate=Gate.UNDETERMINED)]
    assert chain(rows) == [(0, "no_current_task", None)]
