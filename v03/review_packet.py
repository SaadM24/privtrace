import csv,random,json
from pathlib import Path

out=Path("v03/review")
out.mkdir(exist_ok=True)
rows=[r for r in csv.DictReader(open("v03/results/main/language.csv")) if r["split"]=="test" and r["method"]=="dictionary"]
rng=random.Random(953)
chosen=sum((rng.sample([r for r in rows if r["gold_flag"]==gold],n)
            for gold,n in (("True",14),("False",14),("",8))),[])
rng.shuffle(chosen)
cards=[]
key=[]
sites=["Alder","Birch","Cedar","Dune"]
for i,r in enumerate(chosen):
    available=[s for j,s in enumerate(sites) if int(r["prior"])&(1<<j)]
    uid=f"R{i+1:02}"
    cards.append(dict(unit=uid,previously_possible=" / ".join(available),new_statement=r["text"],
                      judgement="",explanation=""))
    key.append(dict(unit=uid,reference=r["gold_flag"] or "unresolved",intent=r["label"]))
for path,rs in ((out/"cards.csv",cards),(Path("v03/results/coordinator.jsonl"),key)):
    if path.suffix==".csv":
        with path.open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=rs[0]);w.writeheader();w.writerows(rs)
    else:
        path.write_text("".join(json.dumps(r)+"\n" for r in rs))
