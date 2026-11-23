from collections import defaultdict
from dataclasses import asdict
from .benchmark import proposals
from .controls import Opening,Offer,decide,schedule


def simulate(s,method,condition,table):
    opening=Opening(tuple(s["visible"]),tuple(s["mail"]),s["quota"],s["cue"])
    order=schedule(method,opening,table)
    state=defaultdict(lambda:15)
    votes=0
    trace=[]
    for e in proposals(s,order):
        who=e["who"]
        mixed=condition in ("mixed","bad_proof")
        lag=s["stale"] if mixed or condition=="lag" else 0
        expired=s["withdraw"] is not None and e["t"]>=s["withdraw"]+lag
        history=state[who]
        sealed=e["asset"]=="sealed"
        claim=e["truth"]
        doc=e["phase"] in ("copy","memo")
        if (mixed or condition=="history") and e["phase"] in ("certify","copy"):
            history=15
        if (mixed or condition=="lineage") and s["bad"] and doc:
            sealed=not sealed
        ok=not ((mixed or condition=="offline") and s["unavailable"] and (doc or e["phase"]=="certify"))
        if method=="checked" and ok:
            expired=s["withdraw"] is not None and e["t"]>=s["withdraw"]
            sealed=e["asset"]=="sealed"
            history=state[who]
            if condition=="bad_proof" and s["bad"]:
                if doc:
                    sealed=False
                if e["phase"]=="certify":
                    history=15
        v=Offer(e["phase"],who,e["purpose"],claim,history,sealed,expired,
                ok if method=="checked" else False,e["message"],votes,s["quota"])
        send,reason=decide(method,v)
        if send:
            state[who]&=e["truth"]
            votes+=int(e["phase"]=="vote")
        trace.append({**e,"view":asdict(v),"sent":send,"reason":reason})
    return asdict(opening),order,trace
