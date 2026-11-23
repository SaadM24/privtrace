import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path
from rescore import inspect


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("results/adaptive"))
    out=p.parse_args().out
    cfg=json.loads(Path("configs/adaptive.json").read_text())
    initial=json.loads(Path("data/table.json").read_text())
    with (out/"cases.jsonl").open() as f:
        cases={s["key"]:s for s in map(json.loads,f)}
    groups={}
    n=0
    with (out/"scores.csv").open() as f,gzip.open(out/"traces.jsonl.gz","rt") as tr:
        history=[]
        last=None
        for r,line in zip(csv.DictReader(f),tr,strict=True):
            x=json.loads(line)
            assert all(str(x[k])==r[k] for k in ("block","period","ordinal","job","regime","method"))
            s=cases[r["job"]]
            if last!=r["job"]:
                if n:
                    history.append(cases[last])
                if r["period"]=="0" and r["ordinal"]=="0":
                    history=[]
                last=r["job"]
            if r["method"]=="recent":
                for cue in ("early","late"):
                    for k in ("A","B"):
                        recent=sum(t["cue"]==cue and t["ticket"]==k for t in history[-cfg["window"]:])
                        wanted=cfg["prior_strength"]*initial[cue][k]/sum(initial[cue].values())+recent
                        assert abs(wanted-x["estimate"][cue][k])<1e-9
            m,bad=inspect(s,x["events"])
            assert all(m[k]==int(r[k]) for k in m)
            assert bad==[v["event"] for v in x["violations"]]
            group=groups.setdefault((r["period"],r["method"],r["regime"]),Counter())
            group.update(n=1,exact=m["exact"],safe_exact=m["safe_exact"],exposure=m["exposure"])
            n+=1
    assert n==len(cases)*8
    with (out/"summary.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["period","method","regime","n","exact","safe_exact","exposure"])
        w.writeheader()
        for (p,m,r),g in groups.items():
            w.writerow(dict(period=p,method=m,regime=r,**g))
    print(f"{n} outcomes verified. Rolling forecasts matched reconstruction from previous closed tickets.")


if __name__=="__main__":
    main()
