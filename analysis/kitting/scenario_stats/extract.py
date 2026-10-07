# analysis/kitting/scenario_stats/extract.py
"""Per-scenario counts of every kitting scenario in the registry, written as JSON (one row per scenario).
Run from the repository root: python analysis/kitting/scenario_stats/extract.py <rows.json>"""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, '.')
from domains.kitting.registry import domain_config as dc
from shared.types import Start, Drop, AfterAction, DuringAction, Now

S = dc['scenarios']; L = dc['layouts']; U = dc['setups']
def load(p): return json.load(open(p))
rows = []
for sid, sc in sorted(S.items()):
    setup = load(U[sc.setup]); lay = load(L[sc.reference_layouts[0]])
    objs = setup['env_objects']; items = [o for o in objs if o['type']=='item']
    dest = {o['id']: o.get('destination') for o in items}
    lt = collections.Counter(o['type'] for o in lay['env_objects'])
    humans = [a for a in sc.agents if a.agent_type=='human']; robots = [a for a in sc.agents if a.agent_type=='robot']
    r = dict(id=sid, setup=sc.setup, layout=sc.reference_layouts[0], nlayouts=len(sc.reference_layouts),
             items=len(items), tables=lt.get('kitting_table',0), shelves=lt.get('shelf',0),
             coffee=lt.get('coffee_machine',0), ac=lt.get('ac_switch',0), landmarks=lt.get('landmark',0),
             areas=len(lay.get('areas',[])), humans=len(humans), robots=len(robots),
             tl_src='scenario' if sc.timeline is not None else ('setup' if setup.get('timeline') else 'none'),
             tl_windows=len(sc.timeline.windows) if sc.timeline is not None else len(setup.get('timeline',[])),
             tl_facts=sorted({w.fact.name for w in sc.timeline.windows} if sc.timeline is not None else {w['fact'] for w in setup.get('timeline',[])}))
    r['robot_tasks'] = sum(len(a.assigned_tasks) for a in robots)
    r['observing_robots'] = sum(1 for a in robots if a.observes)
    h = humans[0] if humans else None
    tc = collections.Counter(); ev = collections.Counter(); dev = 0
    if h:
        scr = h.scheduled_tasks
        r['entries'] = len(scr.entries); r['closing'] = len(scr.closing); r['repeatable'] = len(scr.repeatable)
        r['dependence'] = scr.dependence.value
        for t in scr.tasks(): tc[t.schema.name]+=1
        for e in scr.entries + scr.closing:
            for x in e.events:
                ev['at' if isinstance(x.trigger, AfterAction) else 'during' if isinstance(x.trigger, DuringAction) else 'now'] += 1
                ev['start' if isinstance(x.decision, Start) else 'drop'] += 1
        for t in scr.tasks():
            if t.schema.name=='deliver_item':
                b = {v.name: c.value for v,c in t.bindings.items()}
                tab = [v for k,v in b.items() if 'table' in k]; it=[v for k,v in b.items() if 'item' in k][0]
                if tab and tab[0]!=dest.get(it): dev+=1
        r['h_assigned'] = len(h.assigned_tasks)
        keys = lambda ts: collections.Counter(repr(sorted((v.name,c.value) for v,c in t.bindings.items()))+t.schema.name for t in ts)
        sd = [t for t in scr.tasks() if t.schema.name=='deliver_item']
        r['h_assigned_unperformed'] = sum((keys(h.assigned_tasks)-keys(sd)).values())
        r['h_unassigned_deliveries'] = sum((keys(sd)-keys(h.assigned_tasks)).values())
    else:
        for k in ['entries','closing','repeatable','h_assigned','h_assigned_unperformed','h_unassigned_deliveries']: r[k]=0
        r['dependence']='-'
    r['script_tasks'] = sum(tc.values())
    for k in ['deliver_item','coffee_break','ac_activation','go_to','stand','go_to_and_stand']:
        r['s_'+k] = sum(v for n,v in tc.items() if n==k or (k=='stand' and n in('stand_task',)))
    r['s_foreseeable'] = r['s_coffee_break']+r['s_ac_activation']
    r['s_humanonly'] = r['s_go_to']+r['s_stand']+r['s_go_to_and_stand']
    r['ev_at']=ev['at']; r['ev_during']=ev['during']; r['ev_start']=ev['start']; r['ev_drop']=ev['drop']; r['events']=ev['at']+ev['during']+ev['now']
    r['table_deviation']=dev
    r['foreseeable_hyp'] = r['coffee']+r['ac']
    r['unhandled_items'] = r['items'] - r['robot_tasks'] - r['h_assigned']
    rows.append(r)
print(sorted({n for sc in S.values() for a in sc.agents for t in a.scheduled_tasks.tasks() for n in [t.schema.name]}))
json.dump(rows, open(sys.argv[1],'w'), indent=0)
print(len(rows))
