# analysis/kitting/scenario_stats/summarise.py
"""The distributions and the per-setup table of README.md, from extract.py's rows: python summarise.py <rows.json>"""
import sys
import json, collections, statistics as st
rows = json.load(open(sys.argv[1]))
num = ['items','tables','shelves','coffee','ac','foreseeable_hyp','landmarks','areas','humans','robots','observing_robots','robot_tasks','h_assigned','unhandled_items','entries','closing','repeatable','script_tasks','s_deliver_item','s_coffee_break','s_ac_activation','s_foreseeable','s_go_to','s_stand','s_go_to_and_stand','s_humanonly','events','ev_at','ev_during','ev_start','ev_drop','table_deviation','h_assigned_unperformed','h_unassigned_deliveries','tl_windows','nlayouts']
print(f"{'measure':26s} {'min':>4} {'max':>4} {'mean':>6} {'median':>6} {'sd':>5}  distribution value:count")
for k in num:
    v=[r[k] for r in rows]; c=sorted(collections.Counter(v).items())
    print(f"{k:26s} {min(v):4d} {max(v):4d} {st.mean(v):6.2f} {st.median(v):6.1f} {st.pstdev(v):5.2f}  "+"  ".join(f"{a}:{b}" for a,b in c))
for k in ['tl_src','dependence']:
    print(k, collections.Counter(r[k] for r in rows))
print('tl_facts', collections.Counter(tuple(r['tl_facts']) for r in rows))
print('per setup:', len({r['setup'] for r in rows}), 'per layout:', len({r['layout'] for r in rows}))
for key in ['setup','layout']:
    c=collections.Counter(r[key] for r in rows); print(key, sorted(c.items()))
print('robot idle (0 tasks)', sum(r['robot_tasks']==0 for r in rows))
print('robot x human', sorted(collections.Counter((r['robot_tasks'],r['h_assigned']) for r in rows).items()))
print('foreseeable scripted combos', sorted(collections.Counter((r['s_coffee_break'],r['s_ac_activation']) for r in rows).items()))
print('scen with any event', sum(r['events']>0 for r in rows), 'during', sum(r['ev_during']>0 for r in rows), 'drop', sum(r['ev_drop']>0 for r in rows), 'deviation', sum(r['table_deviation']>0 for r in rows))
print('scripted foreseeable but not in layout', sum((r['s_coffee_break']>0 and r['coffee']==0) or (r['s_ac_activation']>0 and r['ac']==0) for r in rows))
print('items vs (robot+human pools)', sorted(collections.Counter(r['unhandled_items'] for r in rows).items()))
rows=json.load(open(sys.argv[1]))
g=collections.defaultdict(list)
for r in rows: g[r['setup']].append(r)
def rg(v): a,b=min(v),max(v); return f"{a}" if a==b else f"{a}-{b}"
print(f"{'setup':13s} {'n':>3} {'layout(s)':28s} {'it':>3} {'KT':>3} {'cm':>2} {'ac':>2} {'R':>4} {'H':>4} {'ent':>4} {'del':>4} {'cb':>4} {'acA':>4} {'ev':>4} {'drp':>3} {'dev':>3} tl")
for s in sorted(g):
    v=g[s]; L=sorted({r['layout'][-2:] for r in v})
    print(f"{s:13s} {len(v):3d} {','.join(L):28s} {rg([r['items'] for r in v]):>3} {rg([r['tables'] for r in v]):>3} {rg([r['coffee'] for r in v]):>2} {rg([r['ac'] for r in v]):>2} {rg([r['robot_tasks'] for r in v]):>4} {rg([r['h_assigned'] for r in v]):>4} {rg([r['entries'] for r in v]):>4} {rg([r['s_deliver_item'] for r in v]):>4} {rg([r['s_coffee_break'] for r in v]):>4} {rg([r['s_ac_activation'] for r in v]):>4} {sum(r['events']>0 for r in v):4d} {sum(r['ev_drop'] for r in v):3d} {sum(r['table_deviation'] for r in v):3d} "+",".join(f"{k}:{c}" for k,c in collections.Counter(r['tl_src'] for r in v).items()))
