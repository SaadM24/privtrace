from dataclasses import dataclass
from privtrace02.planning import View,choose
from .language import dictionary


@dataclass(frozen=True,slots=True)
class Opening:
    eligible:tuple
    mail:tuple
    quota:int
    cue:str


def schedule(method,v,table):
    slots=list(range(3))
    if method=="cue":
        # Translate the frozen dispatch forecast into a predicted later reviewer.
        view=View(1,v.cue,"optional","a","client",(),1,"public","unqueried",0)
        prefer_early,_=choose("utility",view,table)
        forecast=0 if prefer_early else 1
        return sorted(slots,key=lambda r:r==forecast)
    if method in ("eligible","checked","no_history","text_gate"):
        at_risk={v.mail[i] for i in v.eligible}
        return sorted(slots,key=lambda r:(v.mail[r] in at_risk,r in v.eligible))
    return slots


@dataclass(frozen=True,slots=True)
class Offer:
    phase:str
    observer:str
    purpose:str
    claim:int
    history:int
    sealed:bool
    expired:bool
    verified:bool
    sentence:str
    votes:int
    quota:int


def decide(method,v):
    if v.phase=="prior" or method=="open":
        return True,"delivered"
    if method!="greedy" and v.phase=="vote" and v.votes>=v.quota:
        return False,"quorum satisfied"
    if method=="checked" and not v.verified:
        return False,"no verification"
    if v.sealed and (v.expired or v.observer!="staff"):
        return False,"grant or scope"
    if v.purpose!="service" and v.claim!=15:
        return False,"purpose"
    den=dictionary(v.sentence) if method=="text_gate" else v.claim
    if den is None:
        return False,"unclear wording"
    history=15 if method=="no_history" else v.history
    if v.observer!="staff" and history.bit_count()>1 and (history & den).bit_count()<=1:
        return False,"identifying intersection"
    return True,"delivered"
