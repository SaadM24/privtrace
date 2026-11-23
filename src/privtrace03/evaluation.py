from collections import defaultdict


def score(s,trace):
    histories=defaultdict(lambda:15)
    votes=set()
    certs=set()
    memo=False
    post=blocks=identifications=deliveries=0
    evidence=[]
    for i,e in enumerate(trace):
        who=e["who"]
        old=histories[who]
        after=old&e["truth"]
        identify=who!="staff" and old.bit_count()>1 and after.bit_count()==1
        expired=e["asset"]=="sealed" and s["withdraw"] is not None and s["withdraw"]<=e["t"]
        reasons=[]
        if identify:
            reasons.append("identified")
        if expired:
            reasons.append("expired")
        if e["asset"]=="sealed" and who!="staff":
            reasons.append("scope")
        if e["purpose"]!="service" and e["truth"]!=15:
            reasons.append("purpose")
        if e["sent"]:
            histories[who]=after
            deliveries+=int(e["phase"]!="prior")
            if reasons:
                evidence.append([i,reasons])
            post+=int(expired)
            identifications+=int(identify)
            if e["phase"]=="certify":
                certs.add(e["role"])
            if e["phase"]=="vote":
                votes.add(e["role"])
            memo|=e["phase"]=="memo"
        else:
            blocks+=int(not reasons)
    exact=len(votes)>=s["quota"] and set(s["later"])<=certs and (memo or not s["requires_doc"])
    return dict(exact=int(exact),safe=int(exact and not evidence),exposure=int(bool(evidence)),
                post=int(post>0),identified=identifications,allowed_blocks=blocks,delivered=deliveries),evidence
