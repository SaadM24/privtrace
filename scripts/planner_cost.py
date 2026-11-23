"""Isolate current-view rule and planning costs, excluding logging and the synthetic verifier."""
import csv
import gzip
import json
import statistics
import time
from collections import defaultdict
from pathlib import Path
from privtrace02.planning import View,choose

table=json.loads(Path("data/table.json").read_text())
views=defaultdict(list)
with gzip.open("results/study/traces.jsonl.gz","rt") as f:
    for line in f:
        r=json.loads(line)
        if r["split"]=="test" and r["regime"]=="degraded" and r["method"]!="oracle":
            for e in r["events"]:
                if e["view"]:
                    v=dict(e["view"])
                    v["seen"]=tuple(v["seen"])
                    views[r["method"]].append(View(**v))
with open("results/decision_cost.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["method","decisions_per_pass","passes","median_ns_per_choice"])
    for method,stream in views.items():
        samples=[]
        for _ in range(9):
            start=time.perf_counter_ns()
            for v in stream:
                choose(method,v,table)
            samples.append((time.perf_counter_ns()-start)/len(stream))
        w.writerow([method,len(stream),len(samples),round(statistics.median(samples),1)])
