"""Run from repository root. Creates a fresh output directory."""
import argparse,csv,gzip,json,time
from pathlib import Path
from privtrace03.benchmark import jobs
from privtrace03.experiment import simulate
from privtrace03.evaluation import score


def run(out):
    out.mkdir(parents=True,exist_ok=False)
    cfg=json.loads(Path("v03/config.json").read_text())
    table=json.loads(Path("data/table.json").read_text())
    rows=[]
    cost=[]
    with gzip.open(out/"traces.jsonl.gz","wt") as tr,(out/"cases.jsonl").open("w") as cases:
        for split in ("development","validation","test"):
            for seed in cfg[split]:
                for s in jobs(seed,cfg["jobs_per_seed"],split):
                    cases.write(json.dumps(s)+"\n")
                    for cond in cfg["conditions"]:
                        for method in cfg["methods"]:
                            t=time.perf_counter_ns()
                            opening,order,events=simulate(s,method,cond,table)
                            elapsed=time.perf_counter_ns()-t
                            metrics,ev=score(s,events)
                            key=dict(job=s["id"],split=split,seed=seed,condition=cond,method=method)
                            rows.append({**key,**metrics})
                            cost.append(dict(**key,ns=elapsed))
                            tr.write(json.dumps(dict(**key,opening=opening,order=order,events=events,evidence=ev),separators=(",",":"))+"\n")
    for name,records in (("scores",rows),("timing",cost)):
        with (out/(name+".csv")).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=records[0])
            writer.writeheader()
            writer.writerows(records)
    print(f"{len(rows)} runs across {len({r['job'] for r in rows})} jobs")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    run(p.parse_args().out)
