from collections import defaultdict
from dataclasses import asdict
from .planning import View,choose
from .world import offers,metadata
from .oracle import best


def run(case,regime,method,table):
    events=[]
    history=defaultdict(set)
    target=case["target"]
    other="archive" if target=="client" else "client"
    def append(tick,phase,k,who,action,why,view,route):
        root=("sealed" if case["restricted"] else "routine") if k=="digest" else "slip-"+k
        value=case[k] if k in ("a","b") else "synthetic-document"
        events.append(dict(tick=tick,phase=phase,kind=k,recipient=who,deliver=bool(action),
                           reason=why,view=view,route=route,root=root,value=value))
        if action:
            history[who].add(k)
    for who,prior in ((target,case["prior_target"]),(other,case["prior_other"])):
        if prior:
            append(0,"prior",prior.lower(),who,True,"historical grant",None,[(0,who)])
    candidates=sorted(offers(case),key=lambda e:e["tick"])
    subset=best(case,candidates) if method=="oracle" else None
    for idx,e in enumerate(candidates):
        t,k,who=e["tick"],e["kind"],e["who"]
        ver,claim,proof,live=metadata(case,regime,t,k,method in ("checked","checked_greedy"))
        v=View(t,case["cue"],e["phase"],k,who,tuple(sorted(history[who])),ver,claim,proof,live)
        if subset is None:
            admit,reason=choose(method,v,table)
        else:
            admit,reason=idx in subset,"offline feasible subset"
        append(t,e["phase"],k,who,admit,reason,asdict(v),e["route"])
    return events
