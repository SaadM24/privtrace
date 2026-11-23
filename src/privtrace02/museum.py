"""Separate finite booking manifest, without importing the dispatch generator.
A: packing slip must be staged before closing. B: later courier confirmation.
"""
import random

# A rushed loan is often taken over by a courier. A deferred courier is often
# replaced by collection at the museum, requiring an already staged packing slip.
MANIFEST={
    "early":["B","B","B","A","AB","B","","B"],
    "late":["A","A","A","B","A","AB","A",""],
}


def generate_loans(seed,count):
    rng=random.Random(f"museum-loan-{seed}")
    manifest=[(cue,ticket) for cue,entries in MANIFEST.items() for ticket in entries]
    schedule=(manifest*((count+len(manifest)-1)//len(manifest)))[:count]
    rng.shuffle(schedule)
    for i,(cue,ticket) in enumerate(schedule):
        a=rng.getrandbits(1)
        cohort=rng.getrandbits(1)
        booking="A" if cue=="early" else "B"
        yield dict(key=f"loan-{seed}-{i}",family="loan",seed=seed,cue=cue,booking=booking,
                   changed=booking!=ticket,ticket=ticket,target="archive" if i%3 else "client",
                   prior_target=rng.choice(["","","A","B"]),prior_other=rng.choice(["","B"]),
                   secondary="A" if i%2 else "B",a=a,b=cohort^a,secret=cohort,
                   withdraw=rng.choice([None,5,6]),lag=rng.choice([1,4,7]),
                   restricted=rng.choice([True,True,False]),fault=rng.choice(["honest","unknown","inverted"]),
                   available=rng.random()<.65,staff_required=i%3!=0,
                   route=rng.choice(["relay","fork"]),late_tick=rng.choice([8,9,10]))
