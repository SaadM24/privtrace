"""Online policy interface. No job, clock schedule, dataset reader or evaluator imports."""
from dataclasses import dataclass
from .legacy.rules import adjudicate


@dataclass(frozen=True, slots=True)
class View:
    tick:int
    cue:str
    phase:str
    kind:str
    recipient:str
    seen:tuple
    version:int
    claim:str
    proof:str
    live_version:int


def choose(method,v,table):
    checked=method in ("checked","checked_greedy")
    version=v.version
    restricted=v.claim=="restricted"
    if checked and v.kind=="digest":
        if v.proof=="unavailable":
            return False,"proof unavailable"
        restricted=v.proof=="restricted"
        version=v.live_version
    gate=adjudicate(v.kind,v.recipient,"service",version,v.seen,
                    restricted_ancestor=restricted,lineage=method!="local",history=method!="local")
    if gate!="allow":
        return False,gate
    if v.phase=="optional" and "a" not in v.seen:
        if method=="reserve":
            return False,"reserve"
        if method in ("utility","checked","no_cue"):
            row=table["pooled" if method=="no_cue" else v.cue]
            if row["A"]<=row["B"]:
                return False,"reserve by estimate"
    return True,"admit"
