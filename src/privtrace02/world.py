"""Exogenous source schedule, in-flight routes and currently available metadata."""
def offers(s):
    target=s["target"]
    other="archive" if target=="client" else "client"
    hops={"direct":["intake"],"relay":["intake","broker"],"fork":["intake","switch","relay"]}[s["route"]]
    entries=[(3,"optional","a",target,0),(4,"parallel",s["secondary"].lower(),other,0),
             (6,"staff","digest","desk",2),(7,"copy","digest",other,3)]
    if "B" in s["ticket"]:
        entries.append((s["late_tick"],"request","b",target,s["late_tick"]-1))
    for tick,phase,kind,who,depart in entries:
        route=hops if phase!="request" else ["issuer"]
        # Hops are opaque transit; a trusted recipient gateway mediates all payload access.
        yield dict(tick=tick,phase=phase,kind=kind,who=who,
                   route=[(depart+j,node) for j,node in enumerate(route)]+[(tick,who)])


def metadata(s,regime,tick,kind,verify):
    withdrawal=s["withdraw"]
    expired=withdrawal is not None and tick>=withdrawal
    lag=0 if regime=="clean" else s["lag"]
    observed=withdrawal is not None and tick>=withdrawal+lag
    restricted=s["restricted"] and kind=="digest"
    claim="restricted" if restricted else "public"
    if kind=="digest" and regime=="degraded":
        if s["fault"]=="unknown":
            claim="unknown"
        elif s["fault"]=="inverted":
            claim="public" if restricted else "restricted"
    proof,live="unqueried",0
    if verify and kind=="digest":
        if regime=="clean" or s["available"]:
            proof="restricted" if restricted else "public"
            live=1+int(expired)
        else:
            proof="unavailable"
    return 1+int(observed),claim,proof,live
