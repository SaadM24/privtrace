"""Independent, stdlib-only archive verifier, with no PRIVTRACE imports."""
import argparse
import csv
import gzip
import json
from collections import Counter,defaultdict
from pathlib import Path


def inspect(s,trace,extra=None):
    seen=defaultdict(dict)
    wrong=[]
    expired=[]
    permitted_blocks=0
    for i,e in enumerate(trace):
        role=e["route"][-1][1]
        assert e["tick"]==e["route"][-1][0] and role==e["recipient"]
        k=e["kind"]
        expected_root=("sealed" if s["restricted"] else "routine") if k=="digest" else "slip-"+k
        assert e["root"]==expected_root
        if k in ("a","b"):
            assert e["value"]==s[k]
        staff=role=="desk"
        conflict=k in ("a","b") and not staff and ("a" if k=="b" else "b") in seen[role]
        protected=s["restricted"] and k=="digest"
        stale=protected and s["withdraw"] is not None and s["withdraw"]<=e["tick"]
        forbidden=stale or protected and not staff or conflict
        if e["deliver"] or i==extra:
            if forbidden:
                wrong.append(i)
            if stale:
                expired.append(i)
            seen[role][k]=e["value"]
        else:
            permitted_blocks+=not forbidden
    target=seen[s["target"]]
    complete=set(s["ticket"].lower()).issubset(target) and (not s["staff_required"] or "digest" in seen["desk"])
    combos=[d["a"]!=d["b"] for who,d in seen.items() if who!="desk" and {"a","b"}<=d.keys()]
    return dict(exposure=int(bool(wrong)),post=int(bool(expired)),exact=int(complete),
                safe_exact=int(complete and not wrong),reconstructed=len(combos),
                correct=sum(x==s["secret"] for x in combos),allowed_blocks=permitted_blocks,
                attempted=sum(e["phase"]!="prior" for e in trace),
                delivered=sum(e["phase"]!="prior" and e["deliver"] for e in trace)),wrong


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--study",type=Path,default=Path("results/study"))
    p.add_argument("--data",type=Path,default=Path("data"))
    p.add_argument("--details",type=Path,required=True)
    a=p.parse_args()
    cases={s["key"]:s for path in a.data.glob("*.jsonl") for s in map(json.loads,path.read_text().splitlines())}
    cfg=json.loads(Path("configs/study.json").read_text())
    assert len(cases)==sum(len(cfg[k]) for k in ("development","validation","test","transfer"))*cfg["jobs_per_block"]
    grid={}
    events=0
    with gzip.open(a.study/"traces.jsonl.gz","rt") as tr,(a.study/"scores.csv").open() as f,a.details.open("w",newline="") as d:
        w=None
        for r,line in zip(csv.DictReader(f),tr,strict=True):
            log=json.loads(line)
            assert all(r[k]==str(log[k]) for k in ("job","method","regime","seed","split"))
            s=cases[r["job"]]
            trace=log["events"]
            m,bad=inspect(s,trace)
            assert all(m[k]==int(r[k]) for k in m)
            assert bad==[v["event"] for v in log["violations"]]
            key=(r["job"],r["regime"],r["method"])
            assert key not in grid
            grid[key]=m
            events+=len(trace)
            recoverable=False
            if not m["exact"] and not m["exposure"]:
                recoverable=any(inspect(s,trace,i)[0]["safe_exact"] for i,e in enumerate(trace) if not e["deliver"])
            row={**r,"single_block_recoverable":int(recoverable),"withdrawn":int(s["withdraw"] is not None),
                 "fault":s["fault"],"ticket":s["ticket"] or "none","route":s["route"],
                 "available":int(s["available"]),"prior_target":s["prior_target"] or "none"}
            if w is None:
                w=csv.DictWriter(d,fieldnames=row)
                w.writeheader()
            w.writerow(row)
    for k,s in cases.items():
        # Separate closed-form feasibility condition, without reading comparator actions.
        prior=set(s["prior_target"])
        demand=set(s["ticket"])
        impossible=len(prior|demand)>1 or (s["staff_required"] and s["restricted"]
                                             and s["withdraw"] is not None and s["withdraw"]<=6)
        for regime in cfg["regimes"]:
            ceiling=grid[k,regime,"oracle"]
            assert ceiling["exposure"]==0 and ceiling["exact"]==int(not impossible)
            for method in cfg["methods"]:
                assert grid[k,regime,method]["safe_exact"]<=ceiling["exact"]
    print(f"{len(cases)} jobs; {len(grid)} unique paired rows; {events} event records. All metrics, violation event IDs and oracle ceilings matched.")


if __name__=="__main__":
    main()
