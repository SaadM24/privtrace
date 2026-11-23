import random
from .language import SITES,wording,MASK


def jobs(seed,n,split):
    rng=random.Random(seed)
    for i in range(n):
        site=rng.randrange(4)
        panel=list(range(3))
        rng.shuffle(panel)
        eligible=panel[:1+i%2]
        focus=rng.choice(eligible)
        later=list(eligible) if rng.random()<.25 else [focus]
        topology=("separate","shared","handoff")[i%3]
        mail=["p0","p1","p2"] if topology!="shared" else ["pool","pool","p2"]
        after=mail.copy()
        if topology=="handoff":
            after[focus]=mail[(focus+1)%3]
        cue=("early" if focus==0 else "late") if i%2==0 else rng.choice(["early","late"])
        vertical="north" if site<2 else "south"
        horizontal="coast" if site%2==0 else "inland"
        if rng.choice([True,False]):
            vertical,horizontal=horizontal,vertical
        pre=rng.choice(["neutral","neutral",vertical,horizontal])
        index=rng.choice({"development":[0,1],"validation":[2],"test":[3,4,5]}[split])
        withdraw=rng.choice([None,4,None,6])
        yield dict(id=f"{split}-{seed}-{i}",seed=seed,split=split,site=site,visible=eligible,
                   quota=1+i%2,later=later,mail=mail,after=after,topology=topology,cue=cue,
                   signal="informative" if i%2==0 else "noise",prior=[rng.choice(mail),pre],
                   early=vertical,late=horizontal,style=index,wrap=rng.randrange(3),
                   restricted=rng.random()<.6,requires_doc=rng.random()<.5,
                   withdraw=withdraw,stale=rng.choice([1,3,6]),bad=rng.random()<.4,
                   unavailable=rng.random()<.35,editorial=rng.choice(["service","service","preview"]))


def proposals(s,order):
    def item(t,phase,role,who,label,doc=False,purpose="service"):
        return dict(t=t,phase=phase,role=role,who=who,message=wording(label,s["style"],s["wrap"]),
                    truth=MASK[label],asset="sealed" if doc and s["restricted"] else "ordinary",purpose=purpose)
    who,label=s["prior"]
    yield item(0,"prior",-1,who,label)
    for role in order:
        yield item(1,"vote",role,s["mail"][role],s["early"])
    for role in s["later"]:
        yield item(5,"certify",role,s["after"][role],s["late"])
    yield item(6,"memo",-1,"staff","neutral",True)
    yield item(7,"copy",-1,s["after"][0],s["late"],True,s["editorial"])
