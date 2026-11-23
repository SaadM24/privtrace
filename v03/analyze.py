import argparse,csv,json
from collections import Counter,defaultdict
from pathlib import Path
from statistics import median
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def write(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0])
        w.writeheader()
        w.writerows(rows)


def main(out):
    cfg=json.loads(Path("v03/config.json").read_text())
    cases={s["id"]:s for s in map(json.loads,(out/"cases.jsonl").read_text().splitlines())}
    sums=defaultdict(Counter)
    sub=defaultdict(Counter)
    paired={}
    for r in csv.DictReader((out/"scores.csv").open()):
        s=cases[r["job"]]
        values={k:int(r[k]) for k in ("safe","exact","exposure","post","identified","allowed_blocks","delivered")}
        values.update(n=1,withdrawn=int(s["withdraw"] is not None))
        key=(s["split"],r["condition"],r["method"])
        sums[key].update(values)
        if s["split"]=="test":
            paired[r["job"],r["condition"],r["method"]]=values
            for dim in ("topology","signal","quota"):
                sub[key+(dim,s[dim])].update(values)
    write(out/"summary.csv",[dict(split=k[0],condition=k[1],method=k[2],**v) for k,v in sums.items()])
    write(out/"strata.csv",[dict(split=k[0],condition=k[1],method=k[2],factor=k[3],level=k[4],**v) for k,v in sub.items()])
    effects=[]
    for h,key,x,y in [("H1","safe",("clean","eligible"),("clean","greedy")),
                        ("H2","safe",("clean","eligible"),("clean","minimum")),
                        ("H3","exposure",("mixed","checked"),("mixed","eligible")),
                        ("H4","exposure",("bad_proof","checked"),("mixed","checked"))]:
        blocks=defaultdict(list)
        for s in cases.values():
            if s["split"]=="test":
                blocks[s["seed"]].append(paired[(s["id"],*x)][key]-paired[(s["id"],*y)][key])
        vals=[np.mean(v) for v in blocks.values()]
        draws=np.random.default_rng(cfg["bootstrap_seed"]).choice(vals,(10000,len(vals))).mean(axis=1)
        lo,hi=np.quantile(draws,[.05/8,1-.05/8])
        effects.append(dict(h=h,metric=key,first="/".join(x),second="/".join(y),rd=np.mean(vals),lower=lo,upper=hi))
    write(out/"effects.csv",effects)
    sem=defaultdict(Counter)
    for r in csv.DictReader((out/"language.csv").open()):
        v=sem[r["split"],r["method"]]
        gold,pred=r["gold_flag"],r["pred_flag"]
        if not gold:
            v["ambiguous"]+=1
            v["ambiguous_answered"]+=int(bool(pred))
        elif not pred:
            v["abstain_pos" if gold=="True" else "abstain_neg"]+=1
        else:
            v[{("True","True"):"tp",("False","False"):"tn",("True","False"):"fn",("False","True"):"fp"}[gold,pred]]+=1
    names="tp tn fp fn abstain_pos abstain_neg ambiguous ambiguous_answered".split()
    write(out/"semantics_summary.csv",[dict(split=k[0],method=k[1],**{field:v[field] for field in names}) for k,v in sem.items()])
    costs=defaultdict(list)
    for r in csv.DictReader((out/"timing.csv").open()):
        costs[r["method"]].append(int(r["ns"]))
    write(out/"costs.csv",[dict(method=k,median_us=median(v)/1000,p95_us=np.quantile(v,.95)/1000) for k,v in costs.items()])
    fig,axes=plt.subplots(1,2,figsize=(10,4.4),layout="constrained",sharey=True)
    for ax,cond in zip(axes,("clean","mixed")):
        ms=cfg["methods"]
        pos=np.arange(len(ms))
        for offset,metric,color,name in [(-.17,"safe","#126b64","Safe completion"),(.17,"exposure","#aa5031","Exposure")]:
            ax.barh(pos+offset,[100*sums["test",cond,m][metric]/sums["test",cond,m]["n"] for m in ms],
                    height=.32,color=color,label=name)
        ax.set(yticks=pos,yticklabels=ms,xlim=(0,100),title=cond.capitalize()+" metadata",xlabel="Held-out jobs (%)")
    axes[0].invert_yaxis()
    axes[1].legend(frameon=False)
    fig.savefig(out/"policy_outcomes.pdf")
    plt.close(fig)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    main(p.parse_args().out)
