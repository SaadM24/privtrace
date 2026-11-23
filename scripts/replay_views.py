"""Replay online decisions from whitelisted observations in an isolated subprocess."""
import csv
import gzip
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIELDS="tick cue phase kind recipient seen version claim proof live_version".split()
CHILD="""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from privtrace02.planning import View,choose
table=json.load(open('table.json'))
for line in sys.stdin:
    method,fields=json.loads(line)
    fields['seen']=tuple(fields['seen'])
    print(json.dumps(choose(method,View(**fields),table)))
"""


def main():
    expected=[]
    inputs=[]
    with gzip.open("results/study/traces.jsonl.gz","rt") as f:
        for line in f:
            r=json.loads(line)
            if r["method"]=="oracle":
                continue
            for e in r["events"]:
                if e["view"] is not None:
                    assert sorted(e["view"])==sorted(FIELDS)
                    inputs.append(json.dumps([r["method"],{k:e["view"][k] for k in FIELDS}]))
                    expected.append([e["deliver"],e["reason"]])
    with tempfile.TemporaryDirectory() as dirname:
        folder=Path(dirname)
        dest=folder/"privtrace02"
        (dest/"legacy").mkdir(parents=True)
        for name in ("__init__.py","planning.py","legacy/__init__.py","legacy/rules.py"):
            shutil.copyfile(Path("src/privtrace02")/name,dest/name)
        shutil.copyfile("data/table.json",folder/"table.json")
        (folder/"replay.py").write_text(CHILD)
        result=subprocess.run([sys.executable,"-I","replay.py"],cwd=folder,input="\n".join(inputs)+"\n",
                              capture_output=True,text=True,check=True)
    actual=[json.loads(x) for x in result.stdout.splitlines()]
    if actual!=expected:
        raise ValueError("decisions cannot be reconstructed from the declared view")
    print(f"{len(actual)} online decisions and reason codes exactly reproduced from current fields and frozen counts.")


if __name__=="__main__":
    main()
