"""Gold semantics replay only delivered observer payloads. No imports from policies or world."""
from collections import defaultdict


def score(case,events):
    known=defaultdict(dict)
    illegal=[]
    stale=combos=allowed_blocks=0
    for i,e in enumerate(events):
        who=e["recipient"]
        kind=e["kind"]
        root=e["root"]
        external=who in ("client","archive")
        revoked=root=="sealed" and case["withdraw"] is not None and e["tick"]>=case["withdraw"]
        opposite={"a":"b","b":"a"}.get(kind)
        combo=external and opposite in known[who]
        reasons=[]
        if revoked:
            reasons.append("after withdrawal")
        if external and root=="sealed":
            reasons.append("forbidden ancestor")
        if combo:
            reasons.append("two fragments")
        if e["deliver"]:
            if reasons:
                illegal.append({"event":i,"rules":reasons,"earlier":known[who][opposite][1] if combo else None})
            stale+=int(revoked)
            combos+=int(combo)
            known[who][kind]=(e["value"],i)
        elif not reasons:
            allowed_blocks+=1
    recovered=[k["a"][0]^k["b"][0] for who,k in known.items() if who in ("client","archive") and "a" in k and "b" in k]
    target=known[case["target"]]
    exact=all(x.lower() in target for x in case["ticket"])
    if case["staff_required"]:
        exact=exact and "digest" in known["desk"]
    metrics=dict(exposure=int(bool(illegal)),post=int(stale>0),reconstructed=len(recovered),
                 correct=sum(v==case["secret"] for v in recovered),exact=int(exact),
                 safe_exact=int(exact and not illegal),allowed_blocks=allowed_blocks,
                 delivered=sum(e["deliver"] for e in events if e["phase"]!="prior"),
                 attempted=sum(e["phase"]!="prior" for e in events))
    return metrics,illegal
