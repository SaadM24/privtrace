import argparse
import csv
import gzip
import json
import time
import tracemalloc
from pathlib import Path
from privtrace02.engine import run
from privtrace02.scoring import score


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--data",type=Path,default=Path("data"))
    args=p.parse_args()
    out=args.out
    out.mkdir(parents=True,exist_ok=False)
    cfg=json.loads(Path("configs/study.json").read_text())
    table=json.loads((args.data/"table.json").read_text())
    timer=[]
    first=True
    with (out/"scores.csv").open("w",newline="") as f,gzip.open(out/"traces.jsonl.gz","wt") as tr:
        for split in ("development","validation","test","transfer"):
            for i,line in enumerate((args.data/(split+".jsonl")).read_text().splitlines()):
                case=json.loads(line)
                for regime in cfg["regimes"]:
                    # Rotate fixed order across jobs to spread warm-cache effects.
                    methods=cfg["methods"]
                    offset=i%len(methods)
                    for method in methods[offset:]+methods[:offset]:
                        start=time.perf_counter_ns()
                        events=run(case,regime,method,table)
                        elapsed=time.perf_counter_ns()-start
                        m,violations=score(case,events)
                        key=dict(split=split,seed=case["seed"],job=case["key"],regime=regime,method=method)
                        row={**key,**m}
                        if first:
                            writer=csv.DictWriter(f,fieldnames=row)
                            writer.writeheader()
                            first=False
                        writer.writerow(row)
                        tr.write(json.dumps(dict(**key,events=events,violations=violations),separators=(",",":"))+"\n")
                        # Separate memory pass on a fixed 1/8 sample of each seed block.
                        peak=""
                        if i%8==0:
                            tracemalloc.start()
                            run(case,regime,method,table)
                            _,peak=tracemalloc.get_traced_memory()
                            tracemalloc.stop()
                        timer.append(dict(**key,elapsed_ns=elapsed,peak_bytes=peak))
    with (out/"cost.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=timer[0])
        writer.writeheader()
        writer.writerows(timer)
    print(f"{len(timer)} scored runs; {sum(x['peak_bytes']!='' for x in timer)} separate allocation probes")


if __name__=="__main__":
    main()
