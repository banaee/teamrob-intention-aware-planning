"""
§6.4 hand spot-check of d(t) for s20 prior-on, step 11, candidate item_4, plus
a comparison of projected timing against what the simulator actually did.
Prints the arithmetic; nothing is written.  Usage: python spotcheck.py
"""
import json, math
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
C = json.load(open(HERE / "captures.json"))
cond = next(c for c in C["conditions"] if c["name"] == "s20_on")
tr = next(t for t in cond["triggers"] if t["step"] == 11)
cand = next(c for c in tr["candidates"] if "item_4" in c["task"])
obj = cond["object_positions"]
R0 = tr["agent_positions"]["robot_0"]; H0 = tr["agent_positions"]["human_0"]
print("live positions at trigger: robot", R0, "human", H0)
print("shelf_4", obj["shelf_4"], "shelf_3", obj["shelf_3"], "kitting_table_0", obj["kitting_table_0"])
print("robot segments:", [(s["start_step"], s["end_step"]) for s in cand["projection"]["segments"]])
print("human segments:", [(s["start_step"], s["end_step"]) for s in tr["human_projection"]["segments"]])
d_start_robot = math.dist(R0, obj["shelf_4"]); d_start_human = math.dist(H0, obj["shelf_3"])
d_carry_robot = math.dist(obj["shelf_4"], obj["kitting_table_0"]); d_carry_human = math.dist(obj["shelf_3"], obj["kitting_table_0"])
print(f"robot approach {d_start_robot:.2f} + pick 1 + carry {d_carry_robot:.2f} + place 1 = {d_start_robot+d_carry_robot+2:.2f}  (logged cost {cand['cost']})")
print(f"human approach {d_start_human:.2f} + pick 1 + carry {d_carry_human:.2f} + place 1 = {d_start_human+d_carry_human+2:.2f}")
print(f"robot progress at trigger: {math.dist(cond['object_positions']['shelf_4'], R0):.1f} of 447.2 left; start (-500,300) -> shelf_4 is 447.2; done = {(447.2-d_start_robot)/447.2:.0%}")

def lerp(a, b, f): return (a[0] + f*(b[0]-a[0]), a[1] + f*(b[1]-a[1]))
def robot_at(t):
    if t <= d_start_robot: return lerp(R0, obj["shelf_4"], t/d_start_robot)
    if t <= d_start_robot+1: return tuple(obj["shelf_4"])
    t2 = t - d_start_robot - 1
    if t2 <= d_carry_robot: return lerp(obj["shelf_4"], obj["kitting_table_0"], t2/d_carry_robot)
    return tuple(obj["kitting_table_0"])
def human_at(t):
    if t <= d_start_human: return lerp(H0, obj["shelf_3"], t/d_start_human)
    if t <= d_start_human+1: return tuple(obj["shelf_3"])
    t2 = t - d_start_human - 1
    if t2 <= d_carry_human: return lerp(obj["shelf_3"], obj["kitting_table_0"], t2/d_carry_human)
    return tuple(obj["kitting_table_0"])

curve = pd.read_csv(HERE / "b_curves" / "s20_on_step011.csv", index_col="t")
print("\n t   robot(x,y)          human(x,y)          d by hand   d from analyze.py (b_curves csv)")
for t in (0, 100, 227, 300, 500, 700, 812):
    r, h = robot_at(t), human_at(t)
    print(f"{t:4d}  ({r[0]:7.1f},{r[1]:7.1f})  ({h[0]:7.1f},{h[1]:7.1f})  {math.dist(r,h):9.2f}   {curve.loc[t,'d_item_4']:9.2f}")

# projected timing vs actual execution (Mesa ticks; 1 tick = 20 units of motion, 1 tick per grasp/release)
ticks = cond["ticks"]
grasp = next(t["step"] for t in ticks if t["post_holding"] == "item_4")
done = next(t["step"] for t in ticks if t["step"] > grasp and t["post_holding"] is None)
print(f"\nprojection at step 11: robot pick at t={d_start_robot:.0f} (= {d_start_robot/20:.1f} ticks -> step {11+d_start_robot/20:.1f}); "
      f"place ends at t={cand['cost']} (= {(cand['cost']-2)/20:.1f} motion ticks + 2 -> step {11+(cand['cost']-2)/20+2:.1f})")
print(f"actual: robot holding item_4 from step {grasp}; released at step {done}")
hg = next(t["step"] for t in ticks if t["human_actual_task"] and "item_3" in t["human_actual_task"] and t["step"] > 11 and
          next((x for x in cond['triggers'] if x['step']==t['step']), {}).get('agent_holding', {}).get('human_0') == 'item_3')
print(f"human projection: pick at t={d_start_human:.0f} (-> step {11+d_start_human/20:.1f}); place ends t={tr['human_projection']['total_estimated_cost']} (-> step {11+(tr['human_projection']['total_estimated_cost']-2)/20+2:.1f})")
