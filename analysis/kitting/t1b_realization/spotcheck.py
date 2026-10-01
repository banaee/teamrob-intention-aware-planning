"""
Hand spot-check of one realization: s20 prior-on, step 6 (theta_crossed), candidate
item_4 (the current task), separation s = 30 cm. Prints the arithmetic for the
greedy loop, the exact earliest feasible start and T1's whole shift; compares
each with realize.py. Nothing is written. Usage: python spotcheck.py
"""
import json, math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import realize as R

C = json.load(open(HERE / "captures.json"))
cond = next(c for c in C["conditions"] if c["name"] == "s20_on")
tr = next(t for t in cond["triggers"] if t["step"] == 6)
cand = next(c for c in tr["candidates"] if "item_4" in c["task"])
rp, hp = cand["projection"], tr["human_projection"]
obj = cond["object_positions"]
S = 30.0
R0 = tr["agent_positions"]["robot_0"]; H0 = tr["agent_positions"]["human_0"]
print(f"live positions at the trigger: robot {R0}  human {H0}")
print(f"shelf_4 {obj['shelf_4']}  shelf_3 {obj['shelf_3']}  table {obj['kitting_table_0']}  speed 20 cm/tick, stationary action 1 tick")
print("\nrobot segments (phase, start, end, length):")
for a, s in zip(rp["actions"], rp["segments"]):
    print(f"  {a['phase']:15s} {s['start_step']:7.3f} -> {s['end_step']:7.3f}   {math.dist(s['start_pos'], s['end_pos']):7.2f} cm")
print("human segments:")
for a, s in zip(hp["actions"], hp["segments"]):
    print(f"  {a['phase']:15s} {s['start_step']:7.3f} -> {s['end_step']:7.3f}   {math.dist(s['start_pos'], s['end_pos']):7.2f} cm")
T_h = hp["segments"][-1]["end_step"]
print(f"T_r = {rp['segments'][-1]['end_step']:.3f}  T_h = {T_h:.3f}  (logged cost {cand['cost']})")

# --- the carry segment placed at t0 against the human's carry segment ------
rc = rp["segments"][2]; hc = hp["segments"][2]
P0 = rc["start_pos"]; P1 = rc["end_pos"]; D = rc["end_step"] - rc["start_step"]
v = [(P1[i] - P0[i]) / D for i in range(2)]
Q0 = hc["start_pos"]; Q1 = hc["end_pos"]; c, d = hc["start_step"], hc["end_step"]
w = [(Q1[i] - Q0[i]) / (d - c) for i in range(2)]
t0 = rc["start_step"]
print(f"\nrobot carry placed at t0 = {t0:.3f}, D = {D:.3f}: pos = P0 + v (tau - t0), v = ({v[0]:.3f}, {v[1]:.3f}) cm/tick")
print(f"human carry on [{c:.3f}, {d:.3f}]: pos = Q0 + w (tau - c), w = ({w[0]:.3f}, {w[1]:.3f})")
A = [(P0[i] - v[i] * t0) - (Q0[i] - w[i] * c) for i in range(2)]
B = [v[i] - w[i] for i in range(2)]
aa = A[0]**2 + A[1]**2; ab = A[0]*B[0] + A[1]*B[1]; bb = B[0]**2 + B[1]**2
print(f"relative position A + B tau: A = ({A[0]:.3f}, {A[1]:.3f}), B = ({B[0]:.4f}, {B[1]:.4f})")
print(f"d^2(tau) = {bb:.5f} tau^2 + 2*{ab:.3f} tau + {aa:.1f};   d^2 < {S}^2 = {S*S:.0f}")
disc = ab*ab - bb*(aa - S*S)
r1 = (-ab - math.sqrt(disc)) / bb; r2 = (-ab + math.sqrt(disc)) / bb
lo, hi = max(t0, c), min(t0 + D, d)
print(f"roots {r1:.3f}, {r2:.3f}; overlap window [{lo:.3f}, {hi:.3f}]  ->  violation [{max(r1,lo):.3f}, {min(r2,hi):.3f}], "
      f"open at the window end: {r2 > hi}")
print(f"the window end {hi:.3f} is the ROBOT segment end (t0 + D = {t0+D:.3f}) < T_h = {T_h:.3f}: the robot arrives inside {S:.0f} cm")
print(f"greedy: clear_time = {hi:.3f}; hold = clear_time - t0 = {hi - t0:.3f} ticks (one full carry duration); "
      f"re-check the carry placed at {hi:.3f}: overlap with the human only on [{hi:.3f}, {T_h:.3f}]")
t1 = hi
A1 = [(P0[i] - v[i] * t1) - (Q0[i] - w[i] * c) for i in range(2)]
def dist_at(tau, tstart):
    pr = [P0[i] + v[i] * (tau - tstart) for i in range(2)]
    ph = [Q0[i] + w[i] * (tau - c) for i in range(2)]
    return math.dist(pr, ph)
print(f"   d at tau = T_h with the carry placed at {t1:.3f}: {dist_at(T_h, t1):.2f} cm (the robot has walked {(T_h - t1) * 20:.1f} cm of {D*20:.1f}) -> clear")
hold_ok = R.hold_violation(R.np.array(P0), t0, t1, R.segs(hp), S) is None
print(f"   the hold at shelf_4 {P0} over [{t0:.3f}, {t1:.3f}]: human never within {S:.0f} cm -> {hold_ok}")
print(f"   greedy delta = {t1 - t0:.3f}; realized cost = {rp['segments'][-1]['end_step'] + (t1 - t0):.2f}; placement then starts at {t1 + D:.2f} > T_h (unassessed)")

# --- exact: earliest t' with the carry clear inside the horizon --------------
# with the carry placed at t', at tau = T_h the robot is at P0 + v (T_h - t'); the human is at the
# table (its last segment). Clear iff |P0 + v (T_h - t') - table| >= S, i.e. the robot is still
# >= S cm short of the table at T_h, and no earlier violation.
tbl = obj["kitting_table_0"]
L = math.dist(P0, tbl)
t_star = T_h - (L - S) / 20.0
print(f"\nexact: robot must be >= {S:.0f} cm short of the table at T_h: t' >= T_h - (L - s)/20 = {T_h:.3f} - ({L:.2f} - {S:.0f})/20 = {t_star:.3f}")
print(f"   hold = t' - t0 = {t_star - t0:.3f} ticks  =  (T_h - robot arrival) + s/speed  =  ({T_h:.3f} - {t0 + D:.3f}) + {S:.0f}/20  =  {T_h - (t0 + D):.3f} + {S/20:.2f}")
print(f"   (T1's arrival gap, human placement start minus robot arrival, is {(T_h - 1) - (t0 + D):.3f}; the extra tick is the human's placement, which ends the horizon)")

g = R.realize_greedy(rp, hp, S); e = R.realize_exact(rp, hp, S); w_ = R.realize_whole(rp, hp, S)
print(f"\nrealize.py: greedy delta {g['delta']:.3f} ({g['status']}, holds {[(h[0], round(h[1],3)) for h in g['holds']]});  "
      f"exact delta {e['delta']:.3f};  whole delta {w_['delta']:.3f}")
