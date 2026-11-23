"""Post-hoc feasibility bound. Enumerate early signer sets, omit optional copies.
Later assigned certificates and any commissioned memo must be delivered.
"""
import argparse,csv,json
from itertools import combinations
from collections import defaultdict
from pathlib import Path


def feasible(s):
    if s["requires_doc"] and s["restricted"] and s["withdraw"] is not None and s["withdraw"]<=6:
        return False
    for group in combinations(range(3),s["quota"]):
        history=defaultdict(set)
        who,prior=s["prior"]
        if prior!="neutral":
            history[who].add(prior)
        for i in group:
            history[s["mail"][i]].add(s["early"])
        for i in s["later"]:
            history[s["after"][i]].add(s["late"])
        if max(map(len,history.values()))<=1:
            return True
    return False


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    out=p.parse_args().out
    cases=list(map(json.loads,(out/"cases.jsonl").read_text().splitlines()))
    lookup={s["id"]:feasible(s) for s in cases}
    for r in csv.DictReader((out/"scores.csv").open()):
        assert int(r["safe"])<=lookup[r["job"]]
    with (out/"ceiling.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["job","feasible"]);w.writerows((k,int(v)) for k,v in lookup.items())
    held=[lookup[s["id"]] for s in cases if s["split"]=="test"]
    print(f"{sum(held)}/{len(held)} held-out jobs admit a safe complete schedule under true state.")
