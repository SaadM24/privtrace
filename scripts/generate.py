import argparse
import hashlib
import json
from pathlib import Path
from privtrace02.cases import generate_dispatch
from privtrace02.museum import generate_loans
from privtrace02.training import fit


def write(path,data):
    payload=data.encode()
    if path.exists() and path.read_bytes()!=payload:
        raise ValueError(f"existing artifact differs: {path}")
    path.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("data"))
    out=p.parse_args().out
    out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(Path("configs/study.json").read_text())
    used=set()
    for split in ("development","validation","test","transfer"):
        cases=[]
        factory=generate_loans if split=="transfer" else generate_dispatch
        for seed in cfg[split]:
            assert seed not in used
            used.add(seed)
            for row in factory(seed,cfg["jobs_per_block"]):
                assert row["a"]^row["b"]==row["secret"]
                cases.append(dict(row,split=split))
        if split=="development":
            print("fit",write(out/"table.json",json.dumps(fit(cases),sort_keys=True,indent=2)))
        print(split,len(cases),write(out/(split+".jsonl"),"".join(json.dumps(x,sort_keys=True)+"\n" for x in cases)))


if __name__=="__main__":
    main()
