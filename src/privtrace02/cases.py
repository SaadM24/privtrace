"""Development distribution. Gold jobs are owned by the experiment driver only."""
import random


def generate_dispatch(seed, count):
    rng=random.Random(seed)
    for n in range(count):
        cue=rng.choice(["early","late"])
        original="A" if cue=="early" else "B"
        revised=rng.random()<.2
        ticket=({"A":"B","B":"A"}[original] if revised else original)
        special=rng.random()
        if special<.12:
            ticket="AB"
        elif special<.24:
            ticket=""
        a,b=rng.randrange(2),rng.randrange(2)
        yield dict(key=f"dispatch-{seed}-{n}",family="dispatch",seed=seed,cue=cue,
                   booking=original,changed=ticket!=original,ticket=ticket,
                   target=rng.choice(["client","archive"]),prior_target=rng.choice(["","","","A","B"]),
                   prior_other=rng.choice(["","A","B"]),secondary=rng.choice(["A","B"]),
                   a=a,b=b,secret=a^b,withdraw=rng.choice([None,4,6,None]),
                   lag=rng.choice([0,2,6]),restricted=rng.random()<.6,
                   fault=rng.choice(["honest","honest","unknown","inverted"]),
                   available=rng.random()<.75,staff_required=rng.random()<.45,
                   route=rng.choice(["direct","relay","fork"]),late_tick=rng.choice([7,8,9]))
