import argparse
import csv
import json
from pathlib import Path
from itertools import groupby
from statistics import mean,median
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0])
        w.writeheader()
        w.writerows(rows)


def aggregate(rows,keys):
    fields="exact exposure safe_exact reconstructed correct post allowed_blocks single_block_recoverable delivered attempted".split()
    result=[]
    for labels,group in groupby(sorted(rows,key=lambda r:tuple(r[k] for k in keys)),lambda r:tuple(r[k] for k in keys)):
        g=list(group)
        result.append({**dict(zip(keys,labels)), "n":len(g),"withdrawals":sum(int(r["withdrawn"]) for r in g),
                       **{k:sum(int(r[k]) for r in g) for k in fields}})
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("results"))
    root=p.parse_args().root
    cfg=json.loads(Path("configs/study.json").read_text())
    with (root/"audit_details.csv").open() as f:
        rows=list(csv.DictReader(f))
    sums=aggregate(rows,["split","regime","method"])
    save(root/"summary.csv",sums)
    for field in ("fault","ticket","prior_target","available","route"):
        save(root/(field+".csv"),aggregate(rows,["split","regime","method",field]))
    effects=[]
    for label,regime,metric,first,second in [("H1","clean","exact","utility","full"),("H2","clean","exact","utility","reserve"),
                                            ("H3","degraded","exposure","checked","utility")]:
        subset=[r for r in rows if r["regime"]==regime and r["split"]=="test"]
        values={(r["job"],r["method"]):int(r[metric]) for r in subset}
        blocks={}
        for r in subset:
            if r["method"]==first:
                blocks.setdefault(r["seed"],[]).append(values[r["job"],first]-values[r["job"],second])
        diff=[mean(x) for x in blocks.values()]
        rng=np.random.default_rng(cfg["bootstrap_seed"])
        sims=rng.choice(diff,(cfg["draws"],len(diff))).mean(axis=1)
        lo,hi=np.quantile(sims,[.05/6,1-.05/6])
        effects.append(dict(hypothesis=label,first=first,second=second,metric=metric,regime=regime,
                            blocks=len(blocks),difference=mean(diff),lower=lo,upper=hi,
                            gained=sum(v>0 for b in blocks.values() for v in b),lost=sum(v<0 for b in blocks.values() for v in b)))
    save(root/"primary.csv",effects)
    with (root/"study/cost.csv").open() as f:
        costs=list(csv.DictReader(f))
    perf=[]
    for method in cfg["methods"]:
        g=[r for r in costs if r["method"]==method]
        perf.append(dict(method=method,n=len(g),median_us=median(int(r["elapsed_ns"])/1000 for r in g),
                         p95_us=np.quantile([int(r["elapsed_ns"])/1000 for r in g],.95),
                         peak_sample=sum(bool(r["peak_bytes"]) for r in g),
                         median_peak_bytes=median(int(r["peak_bytes"]) for r in g if r["peak_bytes"])))
    save(root/"performance.csv",perf)
    fig,axes=plt.subplots(1,2,figsize=(10,4.8),layout="constrained",sharey=True)
    methods=cfg["methods"]
    for ax,split in zip(axes,("test","transfer")):
        lookup={r["method"]:r for r in sums if r["split"]==split and r["regime"]=="degraded"}
        y=np.arange(len(methods))
        for metric,offset,color,title in [("safe_exact",-.18,"#09645f","Safe completion"),("exposure",.18,"#b95a32","Any exposure")]:
            ax.barh(y+offset,[100*lookup[m][metric]/lookup[m]["n"] for m in methods],.32,color=color,label=title)
        ax.set(yticks=y,yticklabels=methods,xlim=(0,100),xlabel="Workflows (%)",
               title=("Dispatch test" if split=="test" else "Museum transfer")+" · n = 384")
    axes[0].invert_yaxis()
    axes[1].legend(loc="lower right",frameon=False)
    fig.savefig(root/"degraded_outcomes.pdf")
    plt.close(fig)
    print(effects)
    for r in sums:
        if r["split"] in ("test","transfer"):
            print(*(r[k] for k in ("split","regime","method","n","exact","safe_exact","exposure","post","reconstructed","allowed_blocks","single_block_recoverable")))


if __name__=="__main__":
    main()
