import argparse
import csv
import gzip
import json
from pathlib import Path
from privtrace02.engine import run
from privtrace02.training import fit
from privtrace02.feedback import ClosedTickets
from privtrace02.cases import generate_dispatch
from privtrace02.museum import generate_loans
from privtrace02.scoring import score


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    out=p.parse_args().out
    out.mkdir(parents=True,exist_ok=False)
    cfg=json.loads(Path("configs/adaptive.json").read_text())
    initial=json.loads(Path("data/table.json").read_text())
    with (out/"cases.jsonl").open("w") as raw,(out/"scores.csv").open("w",newline="") as f,gzip.open(out/"traces.jsonl.gz","wt") as tr:
        writer=None
        for seed in cfg["blocks"]:
            history=ClosedTickets(initial,cfg["window"],cfg["prior_strength"])
            for period,generate in enumerate((generate_dispatch,generate_loans,generate_dispatch)):
                for idx,s in enumerate(generate(seed*10+period,cfg["period_size"])):
                    raw.write(json.dumps(s)+"\n")
                    current=history.snapshot()
                    for regime in ("clean","degraded"):
                        for method in cfg["methods"]:
                            tbl={"early":{"A":0,"B":1},"late":{"A":0,"B":1}} if method=="reserve" else (
                                current if method=="recent" else initial)
                            actual="checked_greedy" if method=="greedy" else "checked"
                            events=run(s,regime,actual,tbl)
                            metrics,labels=score(s,events)
                            key=dict(block=seed,period=period,ordinal=idx,job=s["key"],method=method,regime=regime)
                            tr.write(json.dumps(dict(**key,estimate=tbl,events=events,violations=labels))+"\n")
                            row={**key,**metrics}
                            if writer is None:
                                writer=csv.DictWriter(f,fieldnames=row)
                                writer.writeheader()
                            writer.writerow(row)
                    history.close(s["cue"],s["ticket"])


if __name__=="__main__":
    main()
